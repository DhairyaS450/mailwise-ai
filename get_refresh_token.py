from google_auth_oauthlib.flow import InstalledAppFlow
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    # Create flow instance directly from client secrets file
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        SCOPES
    )

    # Run the OAuth flow
    creds = flow.run_local_server(port=5000)

    # Print the refresh token
    print("\nYour refresh token is:\n")
    print(creds.refresh_token)
    print("\nPlease add this to your .env file as GOOGLE_REFRESH_TOKEN=<token>")

if __name__ == '__main__':
    main()
