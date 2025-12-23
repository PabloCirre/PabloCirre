import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_url(url):
    print(f"Checking {url}...")
    try:
        r = requests.get(url)
        
        # 1. Check Doctype
        content_start = r.text.strip()[:15].lower()
        if content_start.startswith('<!doctype html>'):
            print("  ✅ DOCTYPE present")
        else:
            print(f"  ❌ DOCTYPE MISSING or not first! (Starts with: {repr(content_start)})")
            
        # 2. Check CSP Header
        csp = r.headers.get('Content-Security-Policy', '')
        if not csp:
            print("  ❌ CSP Header MISSING")
        else:
            if 'https://www.googletagmanager.com' in csp:
                print("  ✅ CSP includes GTM")
            else:
                print(f"  ❌ CSP MISSING GTM! Value: {csp}")
                
    except Exception as e:
        print(f"  ⚠️ Error: {e}")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://pablocirre.es"
    urls = [
        "/",
        "/bulk-cleaner",
        "/single-email-verification",
        "/pricing",
        "/blog",
        "/contact"
    ]
    
    for path in urls:
        check_url(base_url + path)
