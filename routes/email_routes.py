from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import json
from services.email_service import EmailService
from services.openai_service import generate_daily_summary

email_blueprint = Blueprint('email', __name__)

# OAuth 2.0 configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CLIENT_SECRETS_FILE = "client_secret.json"

@email_blueprint.route('/')
def home():
    if 'credentials' not in session:
        return redirect(url_for('email.login'))
    
    credentials = Credentials(**session['credentials'])
    email_service = EmailService(credentials)
    
    # Fetch and categorize emails
    emails = email_service.fetch_emails(days=1)
    
    # Generate daily summary
    summary = generate_daily_summary(emails)
    
    return render_template('dashboard.html', 
                         emails=emails, 
                         summary=summary)

@email_blueprint.route('/login')
def login():
    if 'credentials' in session:
        return redirect(url_for('email.home'))
        
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('email.oauth2callback', _external=True)
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@email_blueprint.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('email.oauth2callback', _external=True)
    )
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    return redirect(url_for('email.home'))

@email_blueprint.route('/logout')
def logout():
    if 'credentials' in session:
        del session['credentials']
    return redirect(url_for('email.login'))

@email_blueprint.route('/api/custom-rule', methods=['POST'])
def add_custom_rule():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data or 'condition' not in data:
        return jsonify({'error': 'Invalid rule data'}), 400
    
    # Store the custom rule (you might want to use a database here)
    rules = session.get('custom_rules', [])
    rules.append(data)
    session['custom_rules'] = rules
    
    return jsonify({'message': 'Rule added successfully'})