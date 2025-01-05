from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/send-query": {"origins": "*"}})  # Allow all origins

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = 'evolvera.ai.solutions@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'seei thtt yqsb inhx'  # Replace with your email password

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML file for the frontend

@app.route('/send-query', methods=['POST'])
def send_query():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        # Create email content
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"New Query from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'message': 'Query sent successfully!'}), 200

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
