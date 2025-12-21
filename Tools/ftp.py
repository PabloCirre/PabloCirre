import os
import ftplib
import sys
import argparse
import time

# Default Configuration (Fallback / Primary)
FTP_HOST = "ftp.pablocirre.es"
FTP_USER = "pablocirrre"
FTP_PASS = "?De-(vJgBR*5"

LOCAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Parent of Tools/
REMOTE_ROOT = "/"

# Exclusions
IGNORED_DIRS = {'.git', '.secrets', '.vscode', 'Tools', '__pycache__', '.gemini', 'Acredita 2025'}
IGNORED_FILES = {'.gitignore', 'deploy_ftp.ps1', 'deploy_ftp.py', '.DS_Store', 'ftp.py', 'list_ftp.ps1', 'task.md'}

class FTPClient:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password.strip() # Ensure no newlines
        self.ftp = None

    def connect(self):
        # Candidates to try:
        # 1. The provided (host, user, pass)
        # 2. Hardcoded fallback 1 ("pablocirrre")
        # 3. Hardcoded fallback 2 ("pablocirre")
        
        candidates = []
        candidates.append((self.host, self.user, self.password))
        
        # Only add fallbacks IF the provided user is one of the known ones or empty,
        # OR if we want to be safe and try them only after the primary fails.
        # But if the user provided a SPECIFIC new credential, we should probably stick to it.
        
        def_pass = "?De-(vJgBR*5"
        # If the user is NOT the new one provided by the user, we can try fallbacks.
        # This is a bit tricky, let's just make it try the provided one FIRST always.
        
        if self.user not in ["pablocirre@servidor3000.lucusvirtual.es"]:
            if (self.user, self.password) != ("pablocirrre", def_pass):
                 candidates.append((self.host, "pablocirrre", def_pass))
            if (self.user, self.password) != ("pablocirre", def_pass):
                 candidates.append((self.host, "pablocirre", def_pass))
             
        for h, u, p in candidates:
            try:
                print(f"Connecting to {h} with user {u}...")
                p = p.strip() # Ensure no newlines
                if "\n" in p or "\r" in p:
                    print(f"Skipping invalid password with newlines for user {u}")
                    continue
                    
                self.ftp = ftplib.FTP_TLS(h)
                self.ftp.login(u, p)
                self.ftp.prot_p()  # Secure data connection
                print(f"Connected successfully as {u}. PWD: {self.ftp.pwd()}")
                self.host = h
                self.user = u
                self.password = p
                return # Success
            except ftplib.error_perm as e:
                print(f"Login failed for {u}: {e}")
            except Exception as e:
                print(f"Connection error for {u}: {e}")
            
            # Close if partially open
            try: 
                self.ftp.quit() 
            except: 
                pass
            self.ftp = None
            
        print("Error: All login attempts failed.")
        sys.exit(1)

    def get_remote_file_list(self, path=""):
        """Recursively get list of remote files with sizes"""
        if not self.ftp: self.connect()
        
        file_list = {}
        dirs = [path]
        
        print(f"Indexing remote files in {path or '/'}...", end="", flush=True)
        
        while dirs:
            current_dir = dirs.pop()
            rel_dir = current_dir
            if rel_dir.startswith("/"): rel_dir = rel_dir[1:]
            
            try:
                lines = []
                self.ftp.retrlines(f'LIST {current_dir}', lines.append)
                print(".", end="", flush=True)
                
                for line in lines:
                    parts = line.split(maxsplit=8)
                    if len(parts) < 9: continue
                    
                    name = parts[-1]
                    if name in ('.', '..'): continue
                    
                    # Try to parse size (usually 5th field)
                    try:
                        size = int(parts[4])
                    except:
                        size = 0
                        
                    is_dir = line.startswith('d')
                    full_path = f"{current_dir}/{name}" if current_dir else name
                    full_path = full_path.replace("//", "/")
                    
                    if is_dir:
                        dirs.append(full_path)
                    else:
                        # Store relative to search root
                        if path:
                            # If path is set, we want relative to that path
                            key = os.path.relpath(full_path, path).replace("\\", "/")
                        else:
                            key = full_path
                        if key.startswith("/"): key = key[1:]
                        file_list[key] = size
            except Exception as e:
                print(f"Error listing {current_dir}: {e}")
                
        print(" Done.")
        return file_list

    def get_local_file_list(self, path=""):
        """Recursively get list of local files with sizes"""
        file_list = {}
        
        # Resolve absolute path to search
        if path:
             search_root = os.path.abspath(path)
        else:
             search_root = LOCAL_ROOT
             
        if not search_root.startswith(LOCAL_ROOT):
             print(f"Warning: Comparing outside project root {LOCAL_ROOT}")
             
        print(f"Indexing local files in {search_root}...")
        
        tools_exclude = os.path.normpath(os.path.join(LOCAL_ROOT, "Tools"))
        
        for root, dirs, files in os.walk(search_root):
            # Only ignore the GLOBAL Tools directory
            dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) != tools_exclude and d not in (IGNORED_DIRS - {"Tools"})]
            
            for file in files:
                if file in IGNORED_FILES: continue
                
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, search_root)
                rel_path = rel_path.replace("\\", "/")
                
                size = os.path.getsize(abs_path)
                file_list[rel_path] = size
                
        return file_list

    def compare(self, path=""):
        """Compare local and remote files"""
        if not self.ftp: self.connect()
        
        # 1. Get Lists
        print("--- SCARRING REMOTE ---")
        remote_files = self.get_remote_file_list(path)
        print(f"Found {len(remote_files)} remote files.")
        
        print("\n--- SCANNING LOCAL ---")
        local_path = path if path else LOCAL_ROOT #If path arg provided, it maps to local relative 
        if path and not os.path.isabs(path):
            local_path = os.path.join(LOCAL_ROOT, path)
            
        local_files = self.get_local_file_list(local_path)
        print(f"Found {len(local_files)} local files.")
        
        # 2. Compare
        only_local = []
        only_remote = []
        size_mismatch = []
        
        all_keys = set(local_files.keys()) | set(remote_files.keys())
        
        for key in all_keys:
            in_local = key in local_files
            in_remote = key in remote_files
            
            if in_local and not in_remote:
                only_local.append(key)
            elif in_remote and not in_local:
                only_remote.append(key)
            elif in_local and in_remote:
                if local_files[key] != remote_files[key]:
                    size_mismatch.append((key, local_files[key], remote_files[key]))
                    
        # 3. Report
        print("\n=== COMPARISON REPORT ===")
        
        if only_local:
            print("\n[ LOCAL ONLY ] (Missing on Server):")
            for f in sorted(only_local):
                print(f"  + {f}")
        else:
            print("\n[ LOCAL ONLY ]: None")

        if only_remote:
            print("\n[ REMOTE ONLY ] (Extra on Server):")
            for f in sorted(only_remote):
                print(f"  - {f}")
        else:
            print("\n[ REMOTE ONLY ]: None")

        if size_mismatch:
            print("\n[ SIZE MISMATCH ] (Modified?):")
            for f, l_size, r_size in sorted(size_mismatch):
                print(f"  * {f} (Local: {l_size}b | Remote: {r_size}b)")
        else:
            print("\n[ SIZE MISMATCH ]: None")
            
        print("\nDone.")

    def mirror(self, path="", dry_run=False):
        """Mirror local state to remote (DELETE remote files not in local, UPLOAD new/changed)"""
        if not self.ftp: self.connect()
        
        print(f"Starting MIRROR sync for {path or '/'}...")
        if dry_run:
            print("!!! DRY RUN MODE - No changes will be made !!!")
            
        # 1. Get Lists
        remote_files = self.get_remote_file_list(path)
        local_path = path if path else LOCAL_ROOT
        if path and not os.path.isabs(path):
            local_path = os.path.join(LOCAL_ROOT, path)
        local_files = self.get_local_file_list(local_path)
        
        # 2. Identify Actions
        to_delete = []
        to_upload = []
        
        all_keys = set(local_files.keys()) | set(remote_files.keys())
        
        for key in all_keys:
            in_local = key in local_files
            in_remote = key in remote_files
            
            if in_remote and not in_local:
                to_delete.append(key)
            elif in_local and not in_remote:
                to_upload.append(key)
            elif in_local and in_remote:
                if local_files[key] != remote_files[key]:
                    to_upload.append(key)

        print(f"\nFound {len(to_delete)} files to DELETE and {len(to_upload)} files to UPLOAD.")

        # 3. Execute Deletions
        if to_delete:
            print("\n--- DELETING ---")
            for rel_path in sorted(to_delete):
                remote_full_path = f"{path}/{rel_path}" if path else rel_path
                remote_full_path = remote_full_path.replace("//", "/")
                
                if dry_run:
                     print(f"[Dry Run] DELETE: {remote_full_path}")
                else:
                    try:
                        self.ftp.delete(remote_full_path)
                        print(f"Deleted: {remote_full_path}")
                    except Exception as e:
                        print(f"Failed to delete {remote_full_path}: {e}")

        # 4. Execute Uploads
        if to_upload:
            print("\n--- UPLOADING ---")
            for rel_path in sorted(to_upload):
                local_full_path = os.path.join(local_path, rel_path)
                remote_full_path = f"{path}/{rel_path}" if path else rel_path
                remote_full_path = remote_full_path.replace("//", "/")
                
                if dry_run:
                    print(f"[Dry Run] UPLOAD: {local_full_path} -> {remote_full_path}")
                else:
                    remote_dir = os.path.dirname(remote_full_path)
                    if remote_dir and remote_dir != ".":
                        self.ensure_remote_dir(remote_dir)
                    self.upload_file(local_full_path, remote_full_path)
                    
        print("\nMirror sync complete.")

    def close(self):
        if self.ftp:
            try:
                self.ftp.quit()
            except:
                pass

    def list_files(self, path=""):
        if not self.ftp: self.connect()
        print(f"Listing {path or '/'}:")
        try:
            self.ftp.retrlines(f'LIST {path}')
        except Exception as e:
            print(f"Error listing {path}: {e}")

    def ensure_remote_dir(self, remote_dir):
        if not self.ftp: self.connect()
        
        # Clean the path
        remote_dir = remote_dir.replace("\\", "/")
        if remote_dir.startswith("./"):
            remote_dir = remote_dir[2:]
        if remote_dir.startswith("/"):
            remote_dir = remote_dir[1:]
            
        if not remote_dir or remote_dir in [".", ""]: return
        
        parts = remote_dir.split("/")
        current_path = ""
        for part in parts:
            if not part: continue
            
            if current_path:
                current_path += "/"
            current_path += part
            
            try:
                # We try to CWD first to see if it exists
                self.ftp.cwd(current_path)
                self.ftp.cwd("/") # Back to root for next MKD
            except:
                try:
                    self.ftp.mkd(current_path)
                    print(f"Created directory: {current_path}")
                except ftplib.error_perm as e:
                    if "550" not in str(e):
                        print(f"Error creating directory {current_path}: {e}")

    def upload_file(self, local_path, remote_path):
        if not self.ftp: self.connect()
        try:
            # Ensure remote directory exists
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and remote_dir != "/" and remote_dir != ".":
                self.ensure_remote_dir(remote_dir)
                
            with open(local_path, 'rb') as f:
                print(f"Uploading {local_path} -> {remote_path}")
                self.ftp.storbinary(f'STOR {remote_path}', f)
        except Exception as e:
            print(f"Failed to upload {local_path}: {e}")

    def download_file(self, remote_path, local_path):
        if not self.ftp: self.connect()
        try:
            with open(local_path, 'wb') as f:
                print(f"Downloading {remote_path} -> {local_path}")
                self.ftp.retrbinary(f'RETR {remote_path}', f.write)
        except Exception as e:
            print(f"Failed to download {remote_path}: {e}")

    def delete_all(self, path=""):
        """Recursively delete everything in path"""
        if not self.ftp: self.connect()
        
        # Simple safeguard
        if path == "" or path == "/":
            confirm = input("WARNING: You are about to DELETE EVERYTHING on the remote server root. Type 'DELETE' to confirm: ")
            if confirm != "DELETE":
                print("Operation cancelled.")
                return

        print(f"Deleting contents of {path or '/'}...")
        try:
            lines = []
            self.ftp.retrlines(f'LIST {path}', lines.append)
            
            for line in lines:
                parts = line.split(maxsplit=8)
                name = parts[-1]
                if name in ('.', '..'): continue
                
                remote_obj = f"{path}/{name}" if path and path != "/" else name
                
                # Crude detection of directory vs file based on permission string (drwx...)
                is_dir = line.startswith('d')
                
                if is_dir:
                    self.delete_all(remote_obj)
                    try:
                        self.ftp.rmd(remote_obj)
                        print(f"Removed dir: {remote_obj}")
                    except Exception as e:
                        print(f"Failed to remove dir {remote_obj}: {e}")
                else:
                    try:
                        self.ftp.delete(remote_obj)
                        print(f"Deleted file: {remote_obj}")
                    except Exception as e:
                        print(f"Failed to delete file {remote_obj}: {e}")
                        
        except Exception as e:
            print(f"Error during delete_all: {e}")

    def deploy(self, dry_run=False):
        if not self.ftp: self.connect()
        
        print(f"Deploying from {LOCAL_ROOT} to {REMOTE_ROOT}")
        
        for root, dirs, files in os.walk(LOCAL_ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            rel_path = os.path.relpath(root, LOCAL_ROOT)
            if rel_path == ".":
                remote_dir = REMOTE_ROOT
            else:
                remote_dir = os.path.join(REMOTE_ROOT, rel_path).replace("\\", "/")
            
            if not dry_run and remote_dir != "/":
                self.ensure_remote_dir(remote_dir)
            
            for file in files:
                if file in IGNORED_FILES:
                    continue
                
                local_file_path = os.path.join(root, file)
                remote_file_path = f"{remote_dir}/{file}" if remote_dir != "/" else f"/{file}"
                remote_file_path = remote_file_path.replace("//", "/")
                
                if dry_run:
                     print(f"[Dry Run] Upload {local_file_path} -> {remote_file_path}")
                else:
                    self.upload_file(local_file_path, remote_file_path)

    def upload_single(self, path):
        """Uploads a single file or directory recursively"""
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(LOCAL_ROOT):
            print("Error: Can only upload files within the project root.")
            return

        rel_path = os.path.relpath(abs_path, LOCAL_ROOT)

        if rel_path == ".":
            # Uploading root folder content?
            remote_path = REMOTE_ROOT
        else:
            # Join REMOTE_ROOT with relative path
            remote_path = f"{REMOTE_ROOT}/{rel_path}".replace("//", "/")
            remote_path = remote_path.replace("\\", "/") # Normalize slashes

        if os.path.isfile(abs_path):
             self.upload_file(abs_path, remote_path)
        elif os.path.isdir(abs_path):
             # Recursively upload directory
             for root, dirs, files in os.walk(abs_path):
                dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
                curr_rel = os.path.relpath(root, LOCAL_ROOT)
                # Join REMOTE_ROOT with current relative path
                if curr_rel == ".":
                    curr_remote = REMOTE_ROOT
                else:
                    curr_remote = f"{REMOTE_ROOT}/{curr_rel}".replace("//", "/")
                
                curr_remote = curr_remote.replace("\\", "/")
                self.ensure_remote_dir(curr_remote)
                for file in files:
                    if file in IGNORED_FILES: continue
                    f_local = os.path.join(root, file)
                    f_remote = f"{curr_remote}/{file}".replace("//", "/")
                    self.upload_file(f_local, f_remote)


def load_credentials_from_file():
    # Try to find .secrets/ftp_credentials.txt
    secrets_path = os.path.join(LOCAL_ROOT, ".secrets", "ftp_credentials.txt")
    print(f"DEBUG: Looking for secrets at {secrets_path}")
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                content = f.read().strip()
                print("DEBUG: Found secrets file.")
                
                # Check for potential encoding issues (e.g. null bytes often mean UTF-16 read as ANSI/UTF-8)
                if "\x00" in content:
                    print("DEBUG: Detected null bytes, re-reading as UTF-16")
                    with open(secrets_path, "r", encoding="utf-16") as f2:
                         content = f2.read().strip()

                # Try parsing Key=Value or Key: Value
                lines = content.splitlines()
                creds = {}
                for line in lines:
                     if "=" in line:
                         k, v = line.split("=", 1)
                         creds[k.strip().upper()] = v.strip()
                     elif ":" in line:
                         k, v = line.split(":", 1)
                         k = k.strip()
                         # Map common names to our keys
                         if k.lower() == "host": k = "FTP_HOST"
                         if k.lower() == "user": k = "FTP_USER"
                         if k.lower() == "password": k = "FTP_PASS"
                         creds[k.strip().upper()] = v.strip()
                
                if creds:
                    h = creds.get("FTP_HOST", FTP_HOST)
                    u = creds.get("FTP_USER", FTP_USER)
                    p = creds.get("FTP_PASS", FTP_PASS)
                    print(f"DEBUG: Loaded from file (KV/Header) - Host: {h}, User: {u}, PassLen: {len(p) if p else 'None'}")
                    return h, u, p

                # Fallback: Assume entire content is password
                # Sanity check: Passwords shouldn't be massive blobs unless it's a key
                # Increased limit to 200 to allow for long tokens
                if len(content) > 200:
                    print(f"DEBUG: Secrets file content len {len(content)} is suspicious. Content start: {repr(content[:20])}")
                    # Don't return here, try to use it anyway if fallback fails? 
                    # Or return default. Let's return default for safety but log loud.
                    print("DEBUG: Ignoring file due to length.")
                    return FTP_HOST, FTP_USER, FTP_PASS

                print(f"DEBUG: Loaded from file (Raw) - PassLen: {len(content)}")
                return FTP_HOST, FTP_USER, content
        except Exception as e:
            print(f"Warning: Could not read secrets file: {e}")

    print("DEBUG: Using default fallback credentials.")
    return FTP_HOST, FTP_USER, FTP_PASS # Fallbacks

def main():
    parser = argparse.ArgumentParser(description="Unified FTP Tool for PabloCirre")
    parser.add_argument("--user", help="Override FTP user")
    parser.add_argument("--pass", dest="password", help="Override FTP password")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Deploy
    parser_deploy = subparsers.add_parser("deploy", help="Upload changed files (Smart Sync-ish)")
    parser_deploy.add_argument("--dry-run", action="store_true", help="Simulate upload")
    
    # List
    parser_list = subparsers.add_parser("list", help="List remote files")
    parser_list.add_argument("path", nargs="?", default="", help="Remote path to list")

    # Upload
    parser_upload = subparsers.add_parser("upload", help="Upload specific file or folder")
    parser_upload.add_argument("local_path", help="Local path to upload")
    parser_upload.add_argument("remote_path", nargs="?", default=None, help="Remote destination path")
    
    # Delete All
    parser_nuke = subparsers.add_parser("delete-all", help="Delete EVERYTHING on remote")

    # Download
    parser_download = subparsers.add_parser("download", help="Download remote file")
    parser_download.add_argument("remote_path", help="Remote path to download")
    parser_download.add_argument("local_path", help="Local destination path")

    # Compare
    parser_compare = subparsers.add_parser("compare", help="Compare local and remote files")
    parser_compare.add_argument("path", nargs="?", default="", help="Path relative to root to compare")
    
    # Mirror
    parser_mirror = subparsers.add_parser("mirror", help="Mirror local to remote (DELETEs remote-only files)")
    parser_mirror.add_argument("path", nargs="?", default="", help="Path relative to root to mirror")
    parser_mirror.add_argument("--dry-run", action="store_true", help="Simulate changes")

    # Raw List
    parser_raw_list = subparsers.add_parser("raw-list", help="Send raw LIST arguments")
    parser_raw_list.add_argument("args", help="Raw arguments for LIST")

    # Raw Command
    parser_raw = subparsers.add_parser("raw", help="Send raw FTP command")
    parser_raw.add_argument("args", help="Raw command (e.g., 'MKD public_html')")

    args = parser.parse_args()

    # Load credentials
    host, user, password = load_credentials_from_file()
    
    # Overrides
    if args.user: user = args.user
    if args.password: password = args.password

    if not host or not user or not password:
        print("Error: Missing credentials.")
        sys.exit(1)

    client = FTPClient(host, user, password)

    try:
        if args.command == "deploy":
            client.deploy(dry_run=args.dry_run)
        
        elif args.command == "list":
            client.list_files(args.path)
            
        elif args.command == "upload":
            if args.remote_path:
                client.upload_file(args.local_path, args.remote_path)
            else:
                client.upload_single(args.local_path)
            
        elif args.command == "delete-all":
            client.delete_all()

        elif args.command == "download":
            client.download_file(args.remote_path, args.local_path)

        elif args.command == "compare":
            client.compare(args.path)

        elif args.command == "mirror":
            client.mirror(args.path, dry_run=args.dry_run)
            
        elif args.command == "raw-list":
            if not client.ftp: client.connect()
            client.ftp.retrlines(f'LIST {args.args}')
            
        elif args.command == "raw":
            if not client.ftp: client.connect()
            print(f"Sending raw command: {args.args}")
            print(client.ftp.sendcmd(args.args))
            
    finally:
        client.close()

if __name__ == "__main__":
    main()
