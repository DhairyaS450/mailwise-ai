from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from services.openai_service import analyze_email_content
import base64
import email
import html

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
                q=f'after:{time_threshold}',
                maxResults=20  # Limit to 20 emails for better performance
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                try:
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=message['id'],
                        format='full'
                    ).execute()
                    
                    # Process email content
                    headers = msg['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                    from_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
                    date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
                    
                    # Get email body
                    body = self._get_email_body(msg['payload'])
                    
                    # Clean the body text
                    body = self._clean_text(body)
                    
                    # Analyze content using OpenAI
                    category = analyze_email_content(f"Subject: {subject}\n\nContent: {body[:500]}")
                    
                    emails.append({
                        'id': message['id'],
                        'subject': subject,
                        'from': from_email,
                        'date': date,
                        'content': body[:1000] + ('...' if len(body) > 1000 else ''),
                        'category': category
                    })
                    
                except Exception as e:
                    print(f"Error processing individual email: {str(e)}")
                    continue
            
            return emails
            
        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return []

    def _get_email_body(self, payload):
        """Extract email body from the payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode()
                elif 'parts' in part:
                    return self._get_email_body(part)
        elif 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode()
        return ""

    def _clean_text(self, text):
        """Clean and format email text"""
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove very long strings (likely garbage)
        if len(text) > 10000:
            text = text[:10000] + "..."
            
        return text

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