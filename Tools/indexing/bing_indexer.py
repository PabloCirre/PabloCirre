import requests
import xml.etree.ElementTree as ET
import json
import os
import sys
import argparse
from urllib.parse import urlparse

# Configuration Defaults
CONFIG_FILE = "bing_config.json"
URLS_FILE = "urls.txt"
BING_API_ENDPOINT = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch"

def load_config():
    """Load configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), 'bing_config.json')
    if not os.path.exists(config_path):
        print(f"[WARNING] Config file '{CONFIG_FILE}' not found.")
        print(f"Please create it with your API key and Site URL.")
        return None
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Loading config: {e}")
        return None

def fetch_sitemap_urls(sitemap_url):
    """Recursively fetch URLs from sitemap and sitemap index."""
    urls = set()
    print(f"[INFO] Fetching sitemap: {sitemap_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Namespaces (sitemaps usually use this namespace)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Check if it's a Sitemap Index
        if 'sitemapindex' in root.tag:
            print("  → Found Sitemap Index. Fetching children...")
            for sitemap in root.findall('ns:sitemap', ns):
                loc = sitemap.find('ns:loc', ns)
                if loc is not None and loc.text:
                    urls.update(fetch_sitemap_urls(loc.text))
        else:
            # Regular Sitemap
            for url in root.findall('ns:url', ns):
                loc = url.find('ns:loc', ns)
                if loc is not None and loc.text:
                    urls.add(loc.text)
                    
    except Exception as e:
        print(f"[ERROR] Processing {sitemap_url}: {e}")
        
    return list(urls)

def save_urls(urls, filename):
    """Save URLs to a text file."""
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(f"{url}\n")
        print(f"[SUCCESS] Saved {len(urls)} URLs to {filename}")
    except Exception as e:
        print(f"[ERROR] Saving URLs: {e}")

def submit_to_bing(apikey, site_url, url_list):
    """Submit URLs to Bing Webmaster Tools API."""
    print(f"\n[ACTION] Submitting {len(url_list)} URLs to Bing...")
    
    # Bing allows batch submission (limit usually 500 per batch)
    BATCH_SIZE = 500
    
    for i in range(0, len(url_list), BATCH_SIZE):
        batch = url_list[i:i+BATCH_SIZE]
        payload = {
            "siteUrl": site_url,
            "urlList": batch
        }
        
        try:
            url = f"{BING_API_ENDPOINT}?apikey={apikey}"
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                print(f"  [SUCCESS] Batch {i//BATCH_SIZE + 1}: Success! ({len(batch)} URLs)")
            else:
                print(f"  [ERROR] Batch {i//BATCH_SIZE + 1}: Failed ({response.status_code})")
                print(f"     Response: {response.text}")
                
        except Exception as e:
            print(f"  [ERROR] Submitting batch: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate URL list from Sitemap and Index to Bing.")
    parser.add_argument("--sitemap", help="URL of the sitemap (overrides config)")
    parser.add_argument("--dry-run", action="store_true", help="Only generate list, do not submit to Bing")
    args = parser.parse_args()
    
    # Load Config
    config = load_config()
    
    # Determine Sitemap URL
    sitemap_url = args.sitemap
    if not sitemap_url and config:
        sitemap_url = config.get("sitemap_url")
    
    if not sitemap_url:
        print("[ERROR] No sitemap URL provided. Use --sitemap or set it in bing_config.json")
        sys.exit(1)
        
    # 1. Generate URL List
    urls = fetch_sitemap_urls(sitemap_url)
    if not urls:
        print("[WARNING] No URLs found.")
        sys.exit(0)
        
    print(f"[SUCCESS] Found {len(urls)} unique URLs.")
    save_urls(urls, URLS_FILE)
    
    # 2. Submit to Bing
    if args.dry_run:
        print("[INFO] Dry run: Skipping Bing submission.")
        return

    if not config or not config.get("api_key"):
        print("[WARNING] Bing API Key not found in config. Skipping submission.")
        print(f"    URLs are saved in {URLS_FILE}")
        return
        
    submit_to_bing(config["api_key"], config["site_url"], urls)

if __name__ == "__main__":
    main()
