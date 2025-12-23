import ssl
import socket
import datetime

HOST = "pablocirre.es"
PORT = 443

def check_ssl():
    print(f"Checking SSL for {HOST}:{PORT}...")
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                cert = ssock.getpeercert()
                
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                not_after = cert['notAfter']
                
                # Parse date
                expire_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                remaining = expire_date - datetime.datetime.utcnow()
                
                print("\n--- SSL Certificate Details ---")
                print(f"Subject: {subject.get('commonName', 'N/A')}")
                print(f"Issuer: {issuer.get('commonName', 'N/A')}")
                print(f"Organization: {issuer.get('organizationName', 'N/A')}")
                print(f"Expires On: {expire_date}")
                print(f"Days Remaining: {remaining.days}")
                
                if remaining.days < 0:
                    print("STATUS: EXPIRED ❌")
                elif remaining.days < 15:
                    print("STATUS: EXPIRING SOON ⚠️")
                else:
                    print("STATUS: VALID ✅")
                    
    except Exception as e:
        print(f"Error checking SSL: {e}")

if __name__ == "__main__":
    check_ssl()
