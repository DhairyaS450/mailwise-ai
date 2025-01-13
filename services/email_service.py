from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from services.openai_service import analyze_email_content
import base64
import email

class EmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def fetch_emails(self, days=1):
        """Fetch emails from the last specified days"""
        try:
            # Calculate the time threshold
            time_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
            
            # Get messages from Gmail
            results = self.service.users().messages().list(
                userId='me',
                q=f'after:{time_threshold}'
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Process email content
                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
                from_email = next(h['value'] for h in headers if h['name'].lower() == 'from')
                date = next(h['value'] for h in headers if h['name'].lower() == 'date')
                
                # Get email body
                if 'parts' in msg['payload']:
                    parts = msg['payload']['parts']
                    data = parts[0]['body'].get('data', '')
                else:
                    data = msg['payload']['body'].get('data', '')
                
                if data:
                    text = base64.urlsafe_b64decode(data).decode()
                else:
                    text = "No content"
                
                # Analyze content using OpenAI
                category = analyze_email_content(subject + " " + text)
                
                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'from': from_email,
                    'date': date,
                    'content': text,
                    'category': category
                })
            
            return emails
            
        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return []

    def apply_label(self, message_id, label_name):
        """Apply a label to an email"""
        try:
            # Create label if it doesn't exist
            label_id = self._get_or_create_label(label_name)
            
            # Apply label to message
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            
        except Exception as e:
            print(f"Error applying label: {str(e)}")

    def _get_or_create_label(self, label_name):
        """Get or create a Gmail label"""
        try:
            # List all labels
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            # Check if label exists
            for label in labels:
                if label['name'].lower() == label_name.lower():
                    return label['id']
            
            # Create new label
            label = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            created_label = self.service.users().labels().create(
                userId='me',
                body=label
            ).execute()
            
            return created_label['id']
            
        except Exception as e:
            print(f"Error managing label: {str(e)}")
            return None