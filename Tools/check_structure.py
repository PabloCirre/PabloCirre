import os
import ftplib

def main():
    host = "ftp.servidor3000.lucusvirtual.es"
    user = "pablocirre@pablocirre.es"
    password = "?De-(vJgBR*5"

    ftp = ftplib.FTP_TLS(host)
    ftp.login(user, password)
    ftp.prot_p()
    
    print(f"Logged in. PWD: {ftp.pwd()}")
    
    def list_recursive(path, depth=0):
        if depth > 2: return
        try:
            items = []
            ftp.retrlines(f"LIST {path}", items.append)
            for item in items:
                print("  " * depth + item)
                parts = item.split()
                if not parts: continue
                name = parts[-1]
                if item.startswith('d') and name not in ['.', '..']:
                    list_recursive(f"{path}/{name}".replace("//", "/"), depth + 1)
        except Exception as e:
             print("  " * depth + f"! Error listing {path}: {e}")

    list_recursive("/")
    ftp.quit()

if __name__ == "__main__":
    main()
