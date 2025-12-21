import os
import ftplib

def load_creds():
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
    ftp = ftplib.FTP_TLS(host)
    ftp.login(user, password)
    ftp.prot_p()
    
    print(f"Logged in. PWD: {ftp.pwd()}")
    
    def walk(path):
        print(f"\n--- {path} ---")
        try:
            lines = []
            ftp.retrlines(f"LIST {path}", lines.append)
            for l in lines:
                print(f"  {l}")
                parts = l.split()
                if not parts: continue
                name = parts[-1]
                if l.startswith('d') and name not in ['.', '..']:
                    walk(f"{path}/{name}".replace("//", "/"))
        except Exception as e:
            print(f"  FAILED listing {path}: {e}")

    walk("/")
    ftp.quit()

if __name__ == "__main__":
    main()
