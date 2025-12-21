import os
import ftplib
import sys

# Import credential logic from ftp.py if possible, or just copy it
def load_creds():
    # Attempt to load from .secrets/ftp_credentials.txt
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secrets_path = os.path.join(root, ".secrets", "ftp_credentials.txt")
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            content = f.read().strip()
            lines = content.splitlines()
            creds = {}
            for line in lines:
                if "=" in line:
                    k, v = line.split("=", 1)
                    creds[k.strip().upper()] = v.strip()
                elif ":" in line:
                    k, v = line.split(":", 1)
                    creds[k.strip().upper()] = v.strip()
            return creds.get("FTP_HOST"), creds.get("FTP_USER"), creds.get("FTP_PASS")
    return None, None, None

def main():
    host, user, password = load_creds()
    if not host:
        print("Failed to load credentials.")
        return

    print(f"Connecting to {host} as {user}...")
    ftp = ftplib.FTP_TLS(host)
    ftp.login(user, password)
    ftp.prot_p()
    
    print(f"Logged in. PWD: {ftp.pwd()}")
    
    paths_to_probe = [
        "/domains",
        "/domains/pablocirre.es",
        "/domains/pablocirre.es/public_html",
        "/public_html",
        "/www",
        "/httpdocs",
    ]
    
    for p in paths_to_probe:
        print(f"\nProbing {p}...")
        try:
            ftp.cwd(p)
            print(f"  [SUCCESS] CWD to {p}")
            print(f"  PWD is now: {ftp.pwd()}")
            lines = []
            ftp.retrlines("LIST", lines.append)
            print(f"  Found {len(lines)} items.")
            for l in lines[:5]: print(f"    {l}")
        except Exception as e:
            print(f"  [FAILED] {e}")

    ftp.quit()

if __name__ == "__main__":
    main()
