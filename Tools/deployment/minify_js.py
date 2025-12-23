import os
import re

def minify_js(content):
    # Simple JS minifier (remove comments and extra whitespace)
    # Note: This is not a full parser, be careful with regex in JS
    
    # Remove single line comments (careful with URLs)
    # content = re.sub(r'//.*', '', content) # Too risky for URLs
    
    # Remove multi-line comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    
    # Remove whitespace around operators
    # content = re.sub(r'\s*([=+\-\*\/\{\}\(\)\;\,])\s*', r'\1', content)
    
    # Simple approach: remove leading/trailing whitespace per line and empty lines
    lines = content.split('\n')
    minified_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('//'):
            continue
        minified_lines.append(line)
    
    return '\n'.join(minified_lines)

def process_js():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js_dir = os.path.join(base_dir, 'assets', 'js')
    
    for root, dirs, files in os.walk(js_dir):
        for file in files:
            if file.endswith('.js') and not file.endswith('.min.js'):
                # For now, we won't actually rename them to .min.js in the imports because that breaks modules
                # We will just overwrite the file OR strict minifiction if we had a bundler.
                # Since we don't have a bundler, we will just start by "cleaning" them in place or creating a minified copy 
                # but we can't easily switch the imports without parsing.
                
                # allow-list approach: only minify main.js and known modules for now 
                # OR just perform the cleanup.
                
                # Let's create a .min.js for main.js only for now to test
                if file == 'main.js':
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                    
                    minified = minify_js(content)
                    target = path.replace('.js', '.min.js')
                    
                    with open(target, 'w') as f:
                        f.write(minified)
                    print(f"✅ Minified {file} -> {os.path.basename(target)}")

if __name__ == "__main__":
    process_js()
