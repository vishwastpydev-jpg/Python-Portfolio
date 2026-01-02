import os
import base64
import json
import random
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

# --- CONFIGURATION ---
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, ".env_config")
CRED_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

def get_config():
    """Retrieves or asks for Client ID and Secret."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        print("\n--- 🔑 First-Time Setup ---")
        client_id = input("Enter your Google Client ID: ").strip()
        client_secret = input("Enter your Google Client Secret: ").strip()
        config = {"client_id": client_id, "client_secret": client_secret}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return config

def setup_credentials_file():
    """Builds credentials.json from the saved config."""
    config = get_config()
    creds_data = {
        "installed": {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }
    with open(CRED_PATH, 'w') as f:
        json.dump(creds_data, f, indent=4)

def get_gmail_service():
    """Handles authentication and subfolder management."""
    if not os.path.exists(CRED_PATH):
        setup_credentials_file()

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Session expired. Refreshing token...")
            creds.refresh(Request())
        else:
            print("🔑 Opening browser for Google Login...")
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def send_automated_email():
    """Composes and sends the email with an automated feel."""
    try:
        service = get_gmail_service()
        
        print("\n" + "="*40)
        print("         PYTHON MAIL AUTOMATOR")
        print("="*40)
        
        recipient = input("To: ").strip()
        subject = input("Subject: ").strip()
        message_body = input("Message: ").strip()

        # Build the message
        email = EmailMessage()
        email.set_content(message_body)
        email['To'] = recipient
        email['From'] = 'me'
        email['Subject'] = subject

        # Encode (Gmail API Requirement)
        raw_email = base64.urlsafe_b64encode(email.as_bytes()).decode()
        
        print("\n📨 Sending...")
        result = service.users().messages().send(userId="me", body={'raw': raw_email}).execute()
        
        print(f"✅ Success! Message ID: {result['id']}")
        print("="*40)

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    send_automated_email()