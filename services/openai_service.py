import os
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1"  # Explicitly set the base URL
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    raise

def analyze_email_content(content: str) -> str:
    """
    Analyze email content and categorize it as 'Urgent', 'Important', or 'Low Priority'
    """
    try:
        print('Analyze email content')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an email analyzer. Categorize the following email as 'Urgent', 'Important', or 'Low Priority' based on its content and subject."},
                {"role": "user", "content": content}
            ],
            max_tokens=50
        )
        category = response.choices[0].message.content.strip()
        return category if category in ['Urgent', 'Important', 'Low Priority'] else 'Low Priority'
    except Exception as e:
        print(f"Error analyzing email content: {str(e)}")
        return 'Low Priority'

def generate_daily_summary(emails: List[Dict]) -> str:
    """
    Generate a summary of the day's emails using OpenAI
    """
    try:
        if not emails:
            return "No emails to summarize for today."

        # Prepare email data for summarization
        email_summary = "\n".join([
            f"Subject: {email['subject']}\nFrom: {email['from']}\nCategory: {email['category']}\n"
            for email in emails
        ])

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Create a concise summary of today's emails, highlighting the most important messages and urgent matters."},
                {"role": "user", "content": email_summary}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Unable to generate summary at this time."

def analyze_custom_rule(rule: Dict) -> bool:
    """
    Analyze if an email matches a custom rule using OpenAI
    """
    try:
        rule_description = f"Rule: {rule['condition']}\nEmail: {rule['email_content']}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Determine if the email matches the given rule. Respond with 'true' or 'false'."},
                {"role": "user", "content": rule_description}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content.strip().lower() == 'true'
    except Exception as e:
        print(f"Error analyzing custom rule: {str(e)}")
        return False