import os
import re

def minify_css(content):
    # Remove comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Remove whitespace
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s*([\{\}\:\;\,])\s*', r'\1', content)
    content = content.replace(';}', '}')
    return content.strip()

def process_css():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    css_dir = os.path.join(base_dir, 'assets', 'css')
    
    source_file = os.path.join(css_dir, 'style.css')
    target_file = os.path.join(css_dir, 'style.min.css')
    
    if os.path.exists(source_file):
        with open(source_file, 'r') as f:
            content = f.read()
        
        minified = minify_css(content)
        
        with open(target_file, 'w') as f:
            f.write(minified)
            
        print(f"✅ Minified style.css -> style.min.css (Saved {len(content) - len(minified)} bytes)")
    else:
        print("❌ style.css not found")

if __name__ == "__main__":
    process_css()
