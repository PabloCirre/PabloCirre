#!/usr/bin/env python3
"""
IndexNow Bulk URL Submission Tool
Submits all URLs from sitemap to IndexNow for instant indexing on Bing, Yandex, and other engines.

Usage:
    python indexnow_submit.py https://pablocirre.es
"""

import argparse
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from datetime import datetime
import json
import os
import hashlib
import random
import string

TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (IndexNowBot/1.0; +https://pablocirre.es)'

# IndexNow endpoints
INDEXNOW_ENDPOINTS = [
    'https://api.indexnow.org/indexnow',
    'https://www.bing.com/indexnow',
    'https://yandex.com/indexnow',
]


def generate_key():
    """Generate a random IndexNow key."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))


def fetch_sitemap_urls(sitemap_url):
    """Fetch all URLs from sitemap."""
    urls = []
    try:
        response = requests.get(sitemap_url, headers={'User-Agent': USER_AGENT}, timeout=TIMEOUT)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # Check for sitemap index
            for sitemap in root.findall('ns:sitemap', ns):
                loc = sitemap.find('ns:loc', ns)
                if loc is not None:
                    urls.extend(fetch_sitemap_urls(loc.text))
            
            # Regular sitemap
            for url_elem in root.findall('ns:url', ns):
                loc = url_elem.find('ns:loc', ns)
                if loc is not None:
                    urls.append(loc.text)
    except Exception as e:
        print(f"[ERROR] Failed to fetch sitemap: {e}")
    
    return urls


def submit_to_indexnow(host, key, urls, key_location=None):
    """Submit URLs to IndexNow API."""
    print(f"\n[INDEXNOW] Submitting {len(urls)} URLs...")
    
    payload = {
        "host": host,
        "key": key,
        "urlList": urls
    }
    
    if key_location:
        payload["keyLocation"] = key_location
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': USER_AGENT
    }
    
    results = []
    
    for endpoint in INDEXNOW_ENDPOINTS:
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=TIMEOUT
            )
            
            status_map = {
                200: 'OK - URLs submitted successfully',
                202: 'Accepted - URLs will be processed',
                400: 'Bad Request - Invalid format',
                403: 'Forbidden - Key not valid',
                422: 'Unprocessable - URLs not valid',
                429: 'Too Many Requests - Rate limited'
            }
            
            status = status_map.get(response.status_code, f'Unknown ({response.status_code})')
            success = response.status_code in [200, 202]
            
            results.append({
                'endpoint': endpoint,
                'status_code': response.status_code,
                'status': status,
                'success': success
            })
            
            icon = 'OK' if success else 'FAIL'
            print(f"  [{icon}] {endpoint.split('/')[2]}: {status}")
            
            # If one succeeds, that's enough
            if success:
                break
                
        except Exception as e:
            results.append({
                'endpoint': endpoint,
                'status_code': 'ERROR',
                'status': str(e),
                'success': False
            })
            print(f"  [ERR] {endpoint.split('/')[2]}: {e}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='IndexNow Bulk URL Submission')
    parser.add_argument('url', help='Your website URL (e.g., https://pablocirre.es)')
    parser.add_argument('--key', default=None, help='IndexNow key (generates one if not provided)')
    parser.add_argument('--sitemap', default=None, help='Sitemap URL')
    parser.add_argument('--max-urls', type=int, default=100, help='Maximum URLs to submit (default 100)')
    
    args = parser.parse_args()
    
    base_url = args.url.rstrip('/')
    host = base_url.replace('https://', '').replace('http://', '')
    sitemap_url = args.sitemap or f"{base_url}/sitemap.xml"
    
    # Use provided key or generate new one
    key = args.key or generate_key()
    
    print("\n" + "="*60)
    print("INDEXNOW BULK SUBMISSION")
    print("="*60)
    print(f"Site: {base_url}")
    print(f"Host: {host}")
    print(f"Key:  {key}")
    print("="*60)
    
    # Create key file info
    key_file_path = f"{key}.txt"
    print(f"\n[INFO] IndexNow key file needed at: {base_url}/{key_file_path}")
    print(f"[INFO] The file should contain just: {key}")
    
    # Fetch URLs from sitemap
    print(f"\n[SITEMAP] Fetching URLs from {sitemap_url}...")
    urls = fetch_sitemap_urls(sitemap_url)
    
    if not urls:
        print("[ERROR] No URLs found in sitemap!")
        return
    
    print(f"[SUCCESS] Found {len(urls)} URLs")
    
    # Limit URLs
    if len(urls) > args.max_urls:
        urls = urls[:args.max_urls]
        print(f"[INFO] Limited to {args.max_urls} URLs")
    
    # Submit to IndexNow
    results = submit_to_indexnow(host, key, urls)
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"URLs submitted: {len(urls)}")
    print(f"Endpoints tried: {len(results)}")
    print(f"Successful: {success_count}")
    
    if success_count == 0:
        print("\n[!] No successful submissions. Make sure:")
        print(f"    1. File '{key}.txt' exists at {base_url}/{key}.txt")
        print(f"    2. The file contains exactly: {key}")
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'host': host,
        'key': key,
        'urls_submitted': len(urls),
        'urls': urls,
        'results': results
    }
    
    output_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'Reports',
        f'indexnow_report_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUCCESS] Report saved to: {output_path}")
    
    # Return the key for user reference
    return key


if __name__ == '__main__':
    main()
