#!/usr/bin/env python3
"""
Universal FTP Deployment Script
================================
Deploy any website to any FTP server with a simple configuration file.

Usage:
    python deploy_ftp.py

Configuration:
    Create a ftp_config.json file in the same directory with:
    {
        "host": "ftp.yourserver.com",
        "user": "your_username",
        "password": "your_password",
        "preserve": [".well-known", ".ftpquota"],
        "skip_upload": [".git", ".DS_Store", "python", "node_modules"]
    }
"""

import ftplib
import os
import json
import sys
import shutil
import datetime

# Configure stdout for utf-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONFIG_FILE = "config.json"

# Default values if not in config
DEFAULT_PRESERVE = ['.well-known', '.ftpquota', '.', '..']
DEFAULT_SKIP = [
    '.git', '.gitignore', '.DS_Store', '__pycache__', 
    'node_modules', '.env', '.vscode', '.idea',
    'python', 'scripts', 'docs', '*.log'
]

def create_backup(source_dir):
    """Create a zip backup of the project."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = os.path.join(source_dir, 'CopiaSegura')
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
        
    zip_filename = f'pablo_cirre_backup_{timestamp}.zip'
    zip_path = os.path.join(backup_dir, zip_filename)
    
    print(f"\n📦 Creating backup: {zip_filename}")
    
    # Use zipfile to allow exclusions
    import zipfile
    
    EXCLUDE_DIRS = {'CopiaSegura', 'users', '.git', 'node_modules', 'temp', 'vendor', 'AP1S'}
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                # Modify dirs in-place to skip excluded directories
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                
                for file in files:
                    if file == '.DS_Store':
                        continue
                        
                    file_path = os.path.join(root, file)
                    # Avoid zipping the zip file itself if it's being written (though excluded via CopiaSegura check)
                    if file_path == zip_path:
                        continue
                        
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    
        print(f"✅ Backup created successfully at {zip_path}")
    except Exception as e:
        print(f"⚠️  Backup failed: {e}")

def load_config():
    """Load FTP configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file '{CONFIG_FILE}' not found!")
        print(f"\nCreate a {CONFIG_FILE} file with:")
        print("""
{
    "host": "ftp.yourserver.com",
    "user": "your_username",
    "password": "your_password",
    "preserve": [".well-known", ".ftpquota"],
    "skip_upload": [".git", ".DS_Store", "python"]
}
        """)
        sys.exit(1)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required = ['host', 'user', 'password']
        for field in required:
            if field not in config:
                print(f"❌ Missing required field '{field}' in {CONFIG_FILE}")
                sys.exit(1)
        
        # Add defaults if not specified
        config.setdefault('preserve', DEFAULT_PRESERVE)
        config.setdefault('skip_upload', DEFAULT_SKIP)
        
        # Always include . and .. in preserve
        if '.' not in config['preserve']:
            config['preserve'].append('.')
        if '..' not in config['preserve']:
            config['preserve'].append('..')
        
        return config
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {CONFIG_FILE}: {e}")
        sys.exit(1)

def delete_recursive(ftp, path, preserve):
    """Recursively delete files and directories on FTP server."""
    try:
        # Try to change to directory
        ftp.cwd(path)
        # If successful, it's a directory. List contents.
        items = ftp.nlst()
        for item in items:
            if item in ['.', '..']:
                continue
            delete_recursive(ftp, item, preserve)
        ftp.cwd('..')
        ftp.rmd(path)
        print(f"  🗑️  Deleted directory: {path}")
    except ftplib.error_perm:
        # It's a file or empty directory that failed cwd
        try:
            ftp.delete(path)
            print(f"  🗑️  Deleted file: {path}")
        except Exception as e:
            print(f"  ⚠️  Failed to delete {path}: {e}")

def clean_server(ftp, preserve):
    """Clean server keeping only preserved items."""
    print("\n🧹 Cleaning server...")
    try:
        items = ftp.nlst()
        for item in items:
            if item in preserve:
                print(f"  ⏭️  Skipping preserved item: {item}")
                continue
            print(f"  Deleting: {item}")
            delete_recursive(ftp, item, preserve)
    except Exception as e:
        print(f"  ⚠️  Error during cleanup: {e}")

def should_skip(item, skip_list, rel_path=""):
    """Check if item should be skipped based on skip list.
    
    - Simple names like '.git' match anywhere
    - Root-level exclusions: if rel_path is empty and item matches, skip
    - Path patterns: if pattern contains path separator, match against full path
    """
    full_path = os.path.join(rel_path, item) if rel_path else item
    
    for pattern in skip_list:
        if pattern.startswith('*'):
            # Wildcard pattern (e.g., *.log)
            if item.endswith(pattern[1:]):
                return True
        elif os.sep in pattern or '/' in pattern:
            # Path pattern - match against full relative path
            normalized_pattern = pattern.replace('/', os.sep)
            if full_path == normalized_pattern:
                return True
        elif item == pattern:
            # Simple name match - but only at root level for directories like 'Tools'
            # Allow 'Tools' inside other directories (e.g., paginas/Tools)
            if pattern == 'Tools' and rel_path:
                return False  # Don't skip paginas/Tools
            return True
    return False

def upload_recursive(ftp, local_path, skip_list, rel_path=""):
    """Recursively upload files and directories to FTP server."""
    for item in os.listdir(local_path):
        if should_skip(item, skip_list, rel_path):
            if rel_path:
                print(f"  ⏭️  Skipping: {os.path.join(rel_path, item)}")
            else:
                print(f"  ⏭️  Skipping: {item}")
            continue
            
        local_item_path = os.path.join(local_path, item)
        
        if os.path.isdir(local_item_path):
            try:
                ftp.mkd(item)
                print(f"  📁 Created remote directory: {item}")
            except ftplib.error_perm:
                pass # Directory might exist
            
            ftp.cwd(item)
            upload_recursive(ftp, local_item_path, skip_list, os.path.join(rel_path, item))
            ftp.cwd('..')
        else:
            with open(local_item_path, 'rb') as f:
                if rel_path:
                    print(f"  📤 Uploading: {os.path.join(rel_path, item)}")
                else:
                    print(f"  📤 Uploading: {item}")
                ftp.storbinary(f'STOR {item}', f)

def deploy(dry_run=False):
    """Main deployment function."""
    print("🚀 Universal FTP Deployment Script")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    print(f"\n📡 Connecting to {config['host']}...")
    print(f"👤 User: {config['user']}")
    
    try:
        ftp = ftplib.FTP(config['host'])
        ftp.login(config['user'], config['password'])
        print(f"✅ Connected successfully!\n")
        
        # Get current working directory of the script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Go up two levels (python/deployment/ -> python/ -> root/)
        local_root = os.path.dirname(os.path.dirname(script_dir))
        
        print(f"📂 Local root: {local_root}")
        print(f"📂 Remote root: {ftp.pwd()}\n")
        
        # Create Backup
        if not dry_run:
            create_backup(local_root)
        
        # Clean server
        clean_server(ftp, config['preserve'])
        
        # Upload
        print("\n📤 Starting upload...")
        upload_recursive(ftp, local_root, config['skip_upload'])
        
        ftp.quit()
        print("\n" + "=" * 50)
        print("✅ Deployment complete!")
        print("=" * 50)
        
    except ftplib.error_perm as e:
        print(f"\n❌ FTP Permission Error: {e}")
        print("Check your credentials and server permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Universal FTP Deployment Script")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deployment without changes")
    parser.add_argument("--config", help="Path to config file (default: config.json)")
    args = parser.parse_args()

    # Allow custom config path
    global CONFIG_FILE
    if args.config:
        CONFIG_FILE = args.config

    deploy(dry_run=args.dry_run)

if __name__ == "__main__":
    main()

