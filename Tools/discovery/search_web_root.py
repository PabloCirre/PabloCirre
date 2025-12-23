import os
import ftplib
import time

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
    print(f"Connecting to {host} as {user}...")
    ftp = ftplib.FTP_TLS(host)
    ftp.login(user, password)
    ftp.prot_p()
    
    # We will try to find a file that is ALREADY there and matches something unique.
    # Currently we have 'index.php' in root.
    
    # 1. Try to upload a unique file to /
    unique_name = f"verify_{int(time.time())}.txt"
    with open("temp_v.txt", "w") as f: f.write("PROBE")
    
    print(f"Testing write to / as {unique_name}")
    try:
        with open("temp_v.txt", "rb") as f:
            ftp.storbinary(f"STOR /{unique_name}", f)
        print(f"  Successfully uploaded to /{unique_name}")
    except Exception as e:
        print(f"  Failed to upload to /: {e}")

    # 2. Check if it's visible online
    import urllib.request
    url = f"https://pablocirre.es/{unique_name}"
    print(f"Checking {url}")
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                print("  [!!!] SUCCESS! / IS THE WEB ROOT")
            else:
                print(f"  Failed: Status {response.status}")
    except Exception as e:
        print(f"  Failed: {e}")

    # 3. Try common subdirs
    subdirs = ["public_html", "www", "httpdocs", "web"]
    for sd in subdirs:
        print(f"\nTesting {sd}...")
        try:
            ftp.cwd("/")
            ftp.cwd(sd)
            print(f"  Successfully CWD to {sd}")
            with open("temp_v.txt", "rb") as f:
                ftp.storbinary(f"STOR {unique_name}", f)
            print(f"  Uploaded to {sd}/{unique_name}")
            
            url = f"https://pablocirre.es/{unique_name}"
            print(f"  Checking {url}")
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f"  [!!!] SUCCESS! {sd} IS THE WEB ROOT")
                    break
        except Exception as e:
            print(f"  Failed {sd}: {e}")

    ftp.quit()
    if os.path.exists("temp_v.txt"): os.remove("temp_v.txt")

if __name__ == "__main__":
    main()
