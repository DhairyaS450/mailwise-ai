import os
from flask import Flask
from dotenv import load_dotenv
from flask_session import Session
from routes.email_routes import email_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure session
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# OAuth 2.0 configuration
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

# Register blueprints
app.register_blueprint(email_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5000)