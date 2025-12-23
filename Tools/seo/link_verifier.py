#!/usr/bin/env python3
"""
Link Verifier Robot - Pablo Cirre Site Crawler
Crawls all pages from sitemap and verifies internal/external links.

Usage:
    python link_verifier.py https://pablocirre.es
    python link_verifier.py https://pablocirre.es --max-pages 20 --check-external
"""

import argparse
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
TIMEOUT = 10
USER_AGENT = 'Mozilla/5.0 (LinkVerifier/1.0; +https://pablocirre.es)'
HEADERS = {'User-Agent': USER_AGENT}

class LinkVerifier:
    def __init__(self, base_url, check_external=False, max_workers=5):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.check_external = check_external
        self.max_workers = max_workers
        self.visited_urls = set()
        self.results = {
            'pages_checked': 0,
            'links_checked': 0,
            'broken_links': [],
            'working_links': 0,
            'redirects': [],
            'errors': [],
            'pages': []
        }

    def fetch_sitemap(self, sitemap_url=None):
        """Fetch URLs from sitemap."""
        urls = []
        sitemap_locations = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemap/',
        ]
        
        if sitemap_url:
            sitemap_locations.insert(0, sitemap_url.replace(self.base_url, ''))
        
        for loc in sitemap_locations:
            try:
                url = self.base_url + loc
                print(f"[INFO] Trying sitemap: {url}")
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                    root = ET.fromstring(response.content)
                    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                    
                    # Check for sitemap index
                    for sitemap in root.findall('ns:sitemap', ns):
                        loc_elem = sitemap.find('ns:loc', ns)
                        if loc_elem is not None:
                            urls.extend(self.fetch_sitemap(loc_elem.text))
                    
                    # Regular sitemap
                    for url_elem in root.findall('ns:url', ns):
                        loc = url_elem.find('ns:loc', ns)
                        if loc is not None:
                            urls.append(loc.text)
                    
                    if urls:
                        print(f"[SUCCESS] Found {len(urls)} URLs in sitemap")
                        return urls
            except Exception as e:
                continue
        
        # Fallback to just base URL
        if not urls:
            print("[WARNING] No sitemap found, using base URL only")
            urls = [self.base_url + '/']
        
        return urls

    def check_url(self, url):
        """Check if a URL is accessible."""
        try:
            response = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            return {
                'url': url,
                'status': response.status_code,
                'redirect': response.url if response.url != url else None,
                'ok': response.status_code < 400
            }
        except requests.exceptions.Timeout:
            return {'url': url, 'status': 'TIMEOUT', 'ok': False, 'error': 'Connection timeout'}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'status': 'CONNECTION_ERROR', 'ok': False, 'error': 'Connection failed'}
        except Exception as e:
            return {'url': url, 'status': 'ERROR', 'ok': False, 'error': str(e)}

    def extract_links(self, page_url):
        """Extract all links from a page."""
        try:
            response = requests.get(page_url, headers=HEADERS, timeout=TIMEOUT)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                
                # Skip anchors, javascript, mailto
                if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                    continue
                
                # Convert relative to absolute
                full_url = urljoin(page_url, href)
                
                # Determine if internal or external
                is_internal = urlparse(full_url).netloc == self.domain
                
                links.append({
                    'url': full_url,
                    'text': a.get_text(strip=True)[:50],
                    'internal': is_internal
                })
            
            return links
        except Exception as e:
            self.results['errors'].append({'page': page_url, 'error': str(e)})
            return []

    def verify_page(self, page_url):
        """Verify a single page and all its links."""
        if page_url in self.visited_urls:
            return None
        
        self.visited_urls.add(page_url)
        print(f"[CRAWL] Checking: {page_url}")
        
        page_result = {
            'url': page_url,
            'status': None,
            'links': [],
            'broken': []
        }
        
        # Check if page itself is accessible
        page_check = self.check_url(page_url)
        page_result['status'] = page_check['status']
        
        if not page_check['ok']:
            page_result['broken'].append({'url': page_url, 'status': page_check['status']})
            return page_result
        
        # Extract and check links
        links = self.extract_links(page_url)
        page_result['links'] = len(links)
        
        for link in links:
            # Skip external if not checking them
            if not link['internal'] and not self.check_external:
                continue
            
            self.results['links_checked'] += 1
            link_check = self.check_url(link['url'])
            
            if not link_check['ok']:
                broken = {
                    'source_page': page_url,
                    'broken_url': link['url'],
                    'link_text': link['text'],
                    'status': link_check['status'],
                    'internal': link['internal']
                }
                page_result['broken'].append(broken)
                self.results['broken_links'].append(broken)
            else:
                self.results['working_links'] += 1
                if link_check.get('redirect'):
                    self.results['redirects'].append({
                        'from': link['url'],
                        'to': link_check['redirect']
                    })
        
        return page_result

    def run(self, max_pages=None):
        """Run the link verification."""
        print("\n" + "="*60)
        print("LINK VERIFIER ROBOT")
        print(f"Target: {self.base_url}")
        print("="*60 + "\n")
        
        # Get URLs from sitemap
        urls = self.fetch_sitemap()
        
        if max_pages:
            urls = urls[:max_pages]
        
        print(f"\n[INFO] Will check {len(urls)} pages\n")
        
        # Verify each page
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.verify_page, url): url for url in urls}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.results['pages'].append(result)
                    self.results['pages_checked'] += 1
        
        return self.generate_report()

    def generate_report(self):
        """Generate the verification report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'summary': {
                'pages_checked': self.results['pages_checked'],
                'total_links_checked': self.results['links_checked'],
                'working_links': self.results['working_links'],
                'broken_links': len(self.results['broken_links']),
                'redirects': len(self.results['redirects'])
            },
            'broken_links': self.results['broken_links'],
            'redirects': self.results['redirects'][:20],  # Limit redirects in report
            'errors': self.results['errors']
        }
        
        # Print summary
        print("\n" + "="*60)
        print("VERIFICATION COMPLETE")
        print("="*60)
        print(f"Pages checked:     {report['summary']['pages_checked']}")
        print(f"Links checked:     {report['summary']['total_links_checked']}")
        print(f"Working links:     {report['summary']['working_links']}")
        print(f"Broken links:      {report['summary']['broken_links']}")
        print(f"Redirects found:   {report['summary']['redirects']}")
        
        if report['broken_links']:
            print("\n[!] BROKEN LINKS FOUND:")
            for bl in report['broken_links'][:10]:
                print(f"  - {bl['broken_url']}")
                print(f"    Status: {bl['status']} | From: {bl['source_page']}")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='Link Verifier Robot - Crawl and verify all links')
    parser.add_argument('url', help='Base URL to crawl (e.g., https://pablocirre.es)')
    parser.add_argument('--max-pages', type=int, default=None, help='Maximum pages to check')
    parser.add_argument('--check-external', action='store_true', help='Also check external links')
    parser.add_argument('--workers', type=int, default=3, help='Number of concurrent workers')
    parser.add_argument('--output', default=None, help='Output JSON file path')
    
    args = parser.parse_args()
    
    verifier = LinkVerifier(
        base_url=args.url,
        check_external=args.check_external,
        max_workers=args.workers
    )
    
    report = verifier.run(max_pages=args.max_pages)
    
    # Save report
    output_path = args.output or os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'Reports',
        f'link_report_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUCCESS] Report saved to: {output_path}")
    
    # Exit with error code if broken links found
    if report['summary']['broken_links'] > 0:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
