from flask_mail import Message
from backend.shared import mail
from flask import jsonify

def send_email(recipients, subject, body):
    try:
        full_body = f"Hey users!\n\n{body}\n\nBest,\nThe Weight A Minute Team"
        msg = Message(subject, recipients)
        msg.body = full_body
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": {str(e)}}), 500
