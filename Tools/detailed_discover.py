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
    
    print("\n--- MLSD LISTING OF / ---")
    try:
        for name, facts in ftp.mlsd("/"):
            print(f"  {name:20} {facts}")
    except Exception as e:
        print(f"  MLSD FAILED: {e}")

    print("\n--- NLST LISTING OF / ---")
    try:
        names = ftp.nlst("/")
        print(f"  Names found: {names}")
    except Exception as e:
        print(f"  NLST FAILED: {e}")

    # Check for direct domains folder
    try:
        print("\nChecking for 'pablocirre.es/'...")
        names = ftp.nlst("pablocirre.es")
        print(f"  pablocirre.es contents: {names}")
    except: pass

    ftp.quit()

if __name__ == "__main__":
    main()
