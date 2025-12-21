import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
from collections import deque
import concurrent.futures
import time
import sys

# Configuration
START_URL = "https://pablocirre.es"
DOMAIN = "pablocirre.es"
MAX_THREADS = 10
TIMEOUT = 10

# Sets to track state
visited_pages = set()
broken_links = []
checked_urls = {} # URL -> Status Code

class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = set()
        self.assets = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        
        # Hyperlinks
        if tag == 'a' and 'href' in attrs:
            url = urllib.parse.urljoin(self.base_url, attrs['href'])
            self.links.add(url)
            
        # Images, Scripts, Styles
        src_attr = None
        if tag == 'img': src_attr = 'src'
        elif tag == 'script': src_attr = 'src'
        elif tag == 'link' and attrs.get('rel') == 'stylesheet': src_attr = 'href'
        
        if src_attr and src_attr in attrs:
            url = urllib.parse.urljoin(self.base_url, attrs[src_attr])
            self.assets.add(url) # Add to assets checklist

def check_url(url):
    """Checks a single URL and returns status code."""
    if url in checked_urls:
        return checked_urls[url]
        
    try:
        # Fake a user agent to avoid filtering
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        # Try HEAD first
        try:
            req.method = 'HEAD'
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                status = response.getcode()
                checked_urls[url] = status
                return status
        except urllib.error.HTTPError as e:
            if e.code == 405: # Method Not Allowed, try GET
                pass
            else:
                checked_urls[url] = e.code
                return e.code
        except Exception:
            pass # Fallthrough to GET

        # Fallback to GET
        req.method = 'GET'
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            status = response.getcode()
            checked_urls[url] = status
            return status

    except urllib.error.HTTPError as e:
        checked_urls[url] = e.code
        return e.code
    except urllib.error.URLError as e:
        checked_urls[url] = -1 # Connection Error
        return -1
    except Exception as e:
        checked_urls[url] = -2 # Other Error
        return -2

def is_internal(url):
    return DOMAIN in urllib.parse.urlparse(url).netloc

def main():
    print(f"Starting crawl of {START_URL}...")
    print("-" * 50)
    
    queue = deque([START_URL])
    visited_pages.add(START_URL)
    
    # We will process pages one by one to find links,
    # but verify found assets in parallel.
    
    while queue:
        current_url = queue.popleft()
        print(f"Crawling: {current_url}")
        
        try:
            req = urllib.request.Request(
                current_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Parse
                parser = LinkParser(current_url)
                parser.feed(html)
                
                # Identify new internal pages to crawl
                for link in parser.links:
                    # Remove fragment
                    link = urllib.parse.urldefrag(link)[0]
                    
                    if is_internal(link) and link not in visited_pages:
                        # Only crawl typical web pages
                        if link.endswith(('.php', '.html', '/')) or '.' not in link.split('/')[-1]:
                           visited_pages.add(link)
                           queue.append(link)
                
                # Collect ALL items to verify on this page (links + assets)
                items_to_verify = parser.links.union(parser.assets)
                
                # Verify in parallel
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                    future_to_url = {executor.submit(check_url, url): url for url in items_to_verify}
                    
                    for future in concurrent.futures.as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            code = future.result()
                            if code >= 400 or code < 0:
                                print(f"  [BROKEN] {code} - {url}")
                                broken_links.append({
                                    'page': current_url,
                                    'url': url,
                                    'status': code
                                })
                        except Exception as e:
                             print(f"  [ERROR] {e} - {url}")

        except Exception as e:
            print(f"Error fetching page {current_url}: {e}")

    print("-" * 50)
    print("Crawl Complete.")
    print(f"checked {len(checked_urls)} unique URLs.")
    
    if broken_links:
        print(f"\nFound {len(broken_links)} broken links:")
        for item in broken_links:
            print(f"Page: {item['page']}")
            print(f"  Link: {item['url']} (Status: {item['status']})")
    else:
        print("\nNo broken links found!")

if __name__ == "__main__":
    main()
