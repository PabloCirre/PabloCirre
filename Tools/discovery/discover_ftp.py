import os
import ftplib
import sys

def main():
    # Credentials from the conversation
    host = "ftp.servidor3000.lucusvirtual.es"
    user = "pablocirre@pablocirre.es"
    password = "?De-(vJgBR*5"

    ftp = ftplib.FTP_TLS(host)
    ftp.login(user, password)
    ftp.prot_p()
    
    print(f"Logged in. PWD: {ftp.pwd()}")
    
    common_roots = [
        "public_html",
        "www",
        "httpdocs",
        "web",
        "pablocirre.es",
        "pablocirre.es/public_html",
        "domains",
        "domains/pablocirre.es",
        "domains/pablocirre.es/public_html"
    ]
    
    print("\n--- PROBING DIRECTORIES ---")
    for r in common_roots:
        try:
            ftp.cwd("/" + r)
            print(f"[FOUND] /{r} is a valid directory. Content:")
            lines = []
            ftp.retrlines(f"LIST /{r}", lines.append)
            for l in lines[:5]: print(f"  {l}")
            if len(lines) > 5: print(f"  ... ({len(lines)-5} more)")
            ftp.cwd("/")
        except:
            # print(f"[MISS ] /{r}")
            pass

    print("\n--- RECURSIVE LISTING OF ROOT ---")
    lines = []
    ftp.retrlines("LIST -la", lines.append)
    for l in lines:
        print(f"  {l}")

    ftp.quit()

if __name__ == "__main__":
    main()
