#!/usr/bin/env python3
"""
Email Configuration for Trading Simulator
Set up your email credentials here
"""

import os
from email_service import EmailService

def setup_email_config():
    """
    Set up email configuration.
    You can either set environment variables or modify this function.
    """
    
    # Option 1: Set environment variables (recommended for production)
    # export EMAIL_ADDRESS="your-email@gmail.com"
    # export EMAIL_PASSWORD="your-app-password"
    # export SMTP_SERVER="smtp.gmail.com"
    # export SMTP_PORT="587"
    
    # Option 2: Set directly in code (for testing only)
    if not os.getenv('EMAIL_ADDRESS'):
        print("⚠️  Email configuration not found!")
        print("Please set up email configuration:")
        print("1. Set environment variables:")
        print("   export EMAIL_ADDRESS='your-email@gmail.com'")
        print("   export EMAIL_PASSWORD='your-app-password'")
        print("   export SMTP_SERVER='smtp.gmail.com'")
        print("   export SMTP_PORT='587'")
        print("\n2. Or modify email_config.py directly")
        print("\n3. For Gmail, use App Passwords:")
        print("   - Enable 2-factor authentication")
        print("   - Generate an App Password")
        print("   - Use the App Password (not your regular password)")
        return False
    
    return True

def get_email_service():
    """Get configured email service."""
    if setup_email_config():
        return EmailService()
    else:
        return None

# Gmail setup instructions
GMAIL_SETUP_INSTRUCTIONS = """
📧 Gmail Setup Instructions:

1. Enable 2-Factor Authentication:
   - Go to Google Account settings
   - Security → 2-Step Verification
   - Follow the setup process

2. Generate App Password:
   - Go to Google Account settings
   - Security → App passwords
   - Select "Mail" and your device
   - Copy the generated password

3. Set Environment Variables:
   export EMAIL_ADDRESS="your-email@gmail.com"
   export EMAIL_PASSWORD="your-16-character-app-password"
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"

4. Test Configuration:
   python -c "from email_config import get_email_service; print('✅ Email configured!' if get_email_service() else '❌ Email not configured')"
"""

if __name__ == "__main__":
    print(GMAIL_SETUP_INSTRUCTIONS)
