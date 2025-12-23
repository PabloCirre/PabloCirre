import os
import ftplib

def load_creds():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secrets_path = os.path.join(root, ".secrets", "ftp_credentials.txt")
    # I will try both combinations
    return "ftp.servidor3000.lucusvirtual.es", "pablocirrre", "?De-(vJgBR*5"

def main():
    host, user, password = load_creds()
    print(f"Connecting to {host} as {user}...")
    try:
        ftp = ftplib.FTP_TLS(host)
        ftp.login(user, password)
        ftp.prot_p()
        print(f"Logged in! PWD: {ftp.pwd()}")
        lines = []
        ftp.retrlines("LIST", lines.append)
        for l in lines: print(f"  {l}")
        ftp.quit()
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()
