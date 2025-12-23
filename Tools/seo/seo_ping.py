#!/usr/bin/env python3
"""
SEO Ping & Search Engine Submission Tool
Submits your website to search engines and pings blog aggregators for better indexing.

Usage:
    python seo_ping.py https://pablocirre.es
    python seo_ping.py https://pablocirre.es --sitemap https://pablocirre.es/sitemap.xml
"""

import argparse
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, quote
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os

# Configuration
TIMEOUT = 15
USER_AGENT = 'Mozilla/5.0 (SEOPingBot/1.0; +https://pablocirre.es)'
HEADERS = {'User-Agent': USER_AGENT}

# Search Engine Ping URLs (submit sitemaps)
SEARCH_ENGINE_PINGS = {
    'Google': 'https://www.google.com/ping?sitemap={sitemap}',
    'Bing': 'https://www.bing.com/ping?sitemap={sitemap}',
    'IndexNow (Bing/Yandex)': 'https://www.bing.com/indexnow?url={url}&key={key}',
}

# Blog Ping Services (XML-RPC)
BLOG_PING_SERVICES = [
    'http://rpc.pingomatic.com/',
    'http://ping.feedburner.com/',
    'http://blogsearch.google.com/ping/RPC2',
    'http://rpc.weblogs.com/RPC2',
    'http://ping.blogs.yandex.ru/RPC2',
    'http://rpc.technorati.com/rpc/ping',
]

# HTTP GET Ping Services
HTTP_PING_SERVICES = [
    'https://www.feedburner.com/fb/a/pingSubmit?bloglink={url}',
    'http://pingomatic.com/ping/?title={title}&blogurl={url}&rssurl={feed}',
]


class SEOPinger:
    def __init__(self, site_url, sitemap_url=None, indexnow_key=None):
        self.site_url = site_url.rstrip('/')
        self.sitemap_url = sitemap_url or f"{self.site_url}/sitemap.xml"
        self.indexnow_key = indexnow_key
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'site_url': self.site_url,
            'sitemap_url': self.sitemap_url,
            'search_engines': [],
            'blog_pings': [],
            'errors': []
        }

    def ping_search_engines(self):
        """Submit sitemap to major search engines."""
        print("\n[SEARCH ENGINES] Submitting sitemap...")
        
        # Google Ping
        try:
            url = SEARCH_ENGINE_PINGS['Google'].format(sitemap=quote(self.sitemap_url, safe=''))
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            status = 'SUCCESS' if response.status_code == 200 else f'FAILED ({response.status_code})'
            self.results['search_engines'].append({'engine': 'Google', 'status': status})
            print(f"  [{'OK' if response.status_code == 200 else 'FAIL'}] Google Ping: {status}")
        except Exception as e:
            self.results['search_engines'].append({'engine': 'Google', 'status': f'ERROR: {str(e)}'})
            print(f"  [ERROR] Google Ping: {e}")

        # Bing Ping
        try:
            url = SEARCH_ENGINE_PINGS['Bing'].format(sitemap=quote(self.sitemap_url, safe=''))
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            status = 'SUCCESS' if response.status_code == 200 else f'FAILED ({response.status_code})'
            self.results['search_engines'].append({'engine': 'Bing', 'status': status})
            print(f"  [{'OK' if response.status_code == 200 else 'FAIL'}] Bing Ping: {status}")
        except Exception as e:
            self.results['search_engines'].append({'engine': 'Bing', 'status': f'ERROR: {str(e)}'})
            print(f"  [ERROR] Bing Ping: {e}")

        # IndexNow (if key provided)
        if self.indexnow_key:
            try:
                url = f"https://api.indexnow.org/indexnow?url={quote(self.site_url)}&key={self.indexnow_key}"
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                status = 'SUCCESS' if response.status_code in [200, 202] else f'FAILED ({response.status_code})'
                self.results['search_engines'].append({'engine': 'IndexNow', 'status': status})
                print(f"  [{'OK' if response.status_code in [200,202] else 'FAIL'}] IndexNow: {status}")
            except Exception as e:
                self.results['search_engines'].append({'engine': 'IndexNow', 'status': f'ERROR: {str(e)}'})
                print(f"  [ERROR] IndexNow: {e}")

    def ping_blogs_xmlrpc(self, site_title="Pablo Cirre"):
        """Send XML-RPC pings to blog aggregators."""
        print("\n[BLOG PINGS] Sending XML-RPC pings...")
        
        xml_payload = f'''<?xml version="1.0"?>
<methodCall>
  <methodName>weblogUpdates.ping</methodName>
  <params>
    <param><value>{site_title}</value></param>
    <param><value>{self.site_url}</value></param>
  </params>
</methodCall>'''
        
        headers = {
            'Content-Type': 'text/xml',
            'User-Agent': USER_AGENT
        }
        
        for service_url in BLOG_PING_SERVICES:
            try:
                response = requests.post(
                    service_url, 
                    data=xml_payload, 
                    headers=headers, 
                    timeout=TIMEOUT
                )
                if response.status_code == 200:
                    # Check for flerror in response
                    if '<boolean>0</boolean>' in response.text or 'flerror' not in response.text.lower():
                        status = 'SUCCESS'
                    else:
                        status = 'REJECTED'
                else:
                    status = f'FAILED ({response.status_code})'
                    
                self.results['blog_pings'].append({'service': service_url, 'status': status})
                print(f"  [{status[:4]}] {service_url}")
            except requests.exceptions.Timeout:
                self.results['blog_pings'].append({'service': service_url, 'status': 'TIMEOUT'})
                print(f"  [TIME] {service_url}")
            except Exception as e:
                self.results['blog_pings'].append({'service': service_url, 'status': f'ERROR'})
                print(f"  [ERR ] {service_url}")

    def ping_aggregators(self, site_title="Pablo Cirre", feed_url=None):
        """Ping additional aggregator services via HTTP."""
        print("\n[AGGREGATORS] Pinging web services...")
        
        feed = feed_url or f"{self.site_url}/feed/"
        
        aggregators = [
            f"https://feedburner.google.com/fb/a/pingSubmit?bloglink={quote(self.site_url)}",
            f"http://www.moreover.com/ping?u={quote(self.site_url)}",
            f"http://www.weblogalot.com/ping?url={quote(self.site_url)}",
        ]
        
        for url in aggregators:
            try:
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
                status = 'PINGED' if response.status_code in [200, 301, 302] else f'FAILED ({response.status_code})'
                print(f"  [{status[:4]}] {url[:60]}...")
            except Exception as e:
                print(f"  [ERR ] {url[:60]}...")

    def submit_to_directories(self):
        """Print manual submission URLs for web directories."""
        print("\n[DIRECTORIES] Manual submission URLs (open in browser):")
        directories = [
            ('DMOZ Alternative (Curlie)', 'https://curlie.org/docs/en/add.html'),
            ('Bing Webmaster', 'https://www.bing.com/webmasters/submiturl'),
            ('Yandex Webmaster', 'https://webmaster.yandex.com/sites/add/'),
            ('DuckDuckGo', 'https://duckduckgo.com/newbang (uses Bing index)'),
        ]
        
        for name, url in directories:
            print(f"  - {name}: {url}")

    def run(self, site_title="Pablo Cirre"):
        """Execute all pings and submissions."""
        print("\n" + "="*60)
        print("SEO PING & SUBMISSION TOOL")
        print(f"Site: {self.site_url}")
        print(f"Sitemap: {self.sitemap_url}")
        print("="*60)
        
        self.ping_search_engines()
        self.ping_blogs_xmlrpc(site_title)
        self.ping_aggregators(site_title)
        self.submit_to_directories()
        
        # Summary
        se_success = sum(1 for r in self.results['search_engines'] if 'SUCCESS' in r['status'])
        bp_success = sum(1 for r in self.results['blog_pings'] if 'SUCCESS' in r['status'])
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Search Engines Pinged: {se_success}/{len(self.results['search_engines'])}")
        print(f"Blog Services Pinged:  {bp_success}/{len(self.results['blog_pings'])}")
        
        return self.results


def main():
    parser = argparse.ArgumentParser(description='SEO Ping & Search Engine Submission Tool')
    parser.add_argument('url', help='Your website URL (e.g., https://pablocirre.es)')
    parser.add_argument('--sitemap', default=None, help='Sitemap URL (defaults to /sitemap.xml)')
    parser.add_argument('--title', default='Pablo Cirre', help='Site title for blog pings')
    parser.add_argument('--indexnow-key', default=None, help='IndexNow API key for instant indexing')
    parser.add_argument('--output', default=None, help='Output JSON file path')
    
    args = parser.parse_args()
    
    pinger = SEOPinger(
        site_url=args.url,
        sitemap_url=args.sitemap,
        indexnow_key=args.indexnow_key
    )
    
    results = pinger.run(site_title=args.title)
    
    # Save report
    output_path = args.output or os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'Reports',
        f'seo_ping_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUCCESS] Report saved to: {output_path}")


if __name__ == '__main__':
    main()
