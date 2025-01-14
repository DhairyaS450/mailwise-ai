from google.oauth2.credentials import Credentials
import os
from dotenv import load_dotenv

def get_credentials():
    """Create Google OAuth2 credentials from environment variables"""
    load_dotenv()
    
    credentials = {
        'token': None,  # We don't need an access token as we'll use refresh token
        'refresh_token': os.getenv('GOOGLE_REFRESH_TOKEN'),
        'token_uri': os.getenv('GOOGLE_TOKEN_URI'),
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'scopes': ['https://www.googleapis.com/auth/gmail.readonly']
    }
    
    return Credentials(**credentials)
