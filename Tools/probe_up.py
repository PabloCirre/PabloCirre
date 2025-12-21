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
    
    print("\n--- TRYING TO GO UP ---")
    try:
        ftp.cwd("..")
        print(f"  [SUCCESS] CWD to .. | NEW PWD: {ftp.pwd()}")
        lines = []
        ftp.retrlines("LIST", lines.append)
        for l in lines: print(f"    {l}")
    except Exception as e:
        print(f"  [FAILED] Could not go up: {e}")

    print("\n--- LISTING ROOT WITH -a ---")
    lines = []
    try:
        ftp.retrlines("LIST -a", lines.append)
        for l in lines: print(f"    {l}")
    except Exception as e:
        print(f"  [FAILED] LIST -a: {e}")

    ftp.quit()

if __name__ == "__main__":
    main()
