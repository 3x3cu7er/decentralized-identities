from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string 
import random

def generate_otp():
    # Generate a random 6-digit OTP
    return ''.join(random.choices(string.digits, k=6))

def send_email(username, receiver, otp):
    subject = "foundationX, A Revolutionary Decentralized Identity Management Platform"
    dapp_name = "foundationX"
    dapp_url = "http://localhost:8000"
    dapp_description = "shaxMe is a decentralized identity management platform that empowers usernames to control their digital identities and securely interact with blockchain-based applications. By leveraging the power of Ethereum smart contracts and zero-knowledge proofs, shaxMe ensures that usernames' data remains private and secure, while still enabling seamless and transparent interactions with the blockchain ecosystem."

    html_body = f"""
    <html>
    <head>
    </head>
    <body style="color:black">
        <h2>Dear {username},</h2>
        <p>We are thrilled to announce the launch of our new decentralized application (DApp) - {dapp_name}!</p>
        <p>{dapp_description}</p>
        <p>You can access the DApp at:<br>
        <a href="{dapp_url}">{dapp_url}</a></p>
        <p>We believe this DApp will revolutionize the way we interact with the blockchain ecosystem. We invite you to join us and experience the future of decentralized applications.</p>
        <p>If you have any questions or need assistance, please don't hesitate to reach out to us.</p>
        <p>This is your OTP, <strong>{otp}</strong>.<br>
        Don't share with anyone.</p>
        <p>Best regards,<br>
        Your Team at FoundationX</p>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = receiver

    part1 = MIMEText(html_body, 'html')
    msg.attach(part1)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('shaxme49@gmail.com', 'arjubfpdvgdkdzpr ')
        smtp.send_message(msg)

# Usage
username = "Godfred"
receiver = "jupiterciper@gmail.com"
otp_code = generate_otp()




# sending user credentials to email 



def send_user_credential_via_email(user_name, user_email, credential_info):
    # Replace these values with your own SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'shaxme49@gmail.com'
    sender_password = 'arjubfpdvgdkdzpr'

    # Create the email message
    message = EmailMessage()
    message['Subject'] = 'User Credential Information'
    message['From'] = sender_email
    message['To'] = user_email

    # Add the user's name and credential information to the email body
    message.set_content(f"Dear {user_name},\n\nHere are your requested credentials:\n\n{credential_info}\n\nThank you!")

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print(f"Email sent to {user_email} successfully!")






# welcoming emailer 


def send_welcome_email(username, receiver):
    subject = "Welcome to FoundationX, Your Revolutionary Decentralized Identity Management Platform"
    dapp_name = "foundationX"
    dapp_url = "http://localhost:8000"
    dapp_description = "shaxMe is a decentralized identity management platform that empowers usernames to control their digital identities and securely interact with blockchain-based applications. By leveraging the power of Ethereum smart contracts and zero-knowledge proofs, shaxMe ensures that usernames' data remains private and secure, while still enabling seamless and transparent interactions with the blockchain ecosystem."

    html_body = f"""
    <html>
    <head>
    </head>
    <body style="color:black">
        <h2>Dear {username},</h2>
        <p>Welcome to FoundationX, your revolutionary decentralized identity management platform!</p>
        <p>{dapp_description}</p>
        <p>You can access the DApp at:<br>
        <a href="{dapp_url}">{dapp_url}</a></p>
        <p>We believe this DApp will revolutionize the way you interact with the blockchain ecosystem. We invite you to join us and experience the future of decentralized applications.</p>
        <p>If you have any questions or need assistance, please don't hesitate to reach out to us.</p>
        <p>Best regards,<br>
        Your Team at FoundationX</p>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = receiver

    part1 = MIMEText(html_body, 'html')
    msg.attach(part1)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('shaxme49@gmail.com', 'arjubfpdvgdkdzpr ')
        smtp.send_message(msg)

# Usage
username = "Godfred"
receiver = "jupiterciper@gmail.com"



def send_reset_password_email(username, receiver, otp):
    subject = "Reset Your Password - foundationX"
    dapp_name = "foundationX"
    dapp_url = "http://localhost:8000/verify email"

    html_body = f"""
    <html>
    <head>
    </head>
    <body style="color:black">
        <h2>Dear {username},</h2>
        <p>We have received a request to reset your password for your {dapp_name} account.</p>
        <p>Please use the following one-time password (OTP) to complete the password reset process:</p>
        <p><strong>{otp}</strong></p>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>To reset your password, click the following link and enter the OTP:</p>
        <p><a href="{dapp_url}">{dapp_url}</a></p>
        <p>Best regards,<br>
        Your Team at FoundationX</p>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = receiver

    part1 = MIMEText(html_body, 'html')
    msg.attach(part1)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('shaxme49@gmail.com', 'arjubfpdvgdkdzpr ')
        smtp.send_message(msg)

# Usage
username = "Godfred"
receiver = "jupiterciper@gmail.com"
otp_code = generate_otp()  # Assuming generate_otp() function is defined elsewhere