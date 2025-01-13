# Email Management App

A web-based email management application that uses AI to categorize emails and generate summaries. Built with Flask and integrated with Gmail and OpenAI APIs.

## Features

- Gmail OAuth 2.0 Authentication
- AI-powered email categorization (Urgent, Important, Low Priority)
- Daily email summaries
- Custom rules engine for email categorization
- Modern, responsive dashboard interface

## Prerequisites

- Python 3.8+
- Gmail API credentials
- OpenAI API key

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd email-management-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google OAuth 2.0:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the client configuration file and save it as `client_secret.json` in the project root

4. Configure environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     OPENAI_API_KEY=your_openai_api_key
     ```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Login with your Gmail account
2. View categorized emails on the dashboard
3. Read the daily summary of your emails
4. Create custom rules for email categorization
5. Filter emails by category

## Security

- Uses OAuth 2.0 for secure Gmail authentication
- Environment variables for sensitive credentials
- Session-based authentication
- HTTPS recommended for production deployment

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License
