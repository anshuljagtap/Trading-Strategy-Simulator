#!/usr/bin/env python3
"""
Email Service for Trading Simulator
Handles sending emails for password reset and welcome messages
"""

import smtplib
import ssl
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        """Initialize the email service."""
        # Email configuration - you can set these as environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_address = os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com')
        self.email_password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
        self.app_name = "Trading Strategy Simulator"
        
    def generate_reset_token(self, length=32):
        """Generate a secure reset token."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def send_welcome_email(self, user_email, username):
        """Send a welcome email to new users."""
        try:
            subject = f"Welcome to {self.app_name}! 🎉"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1f77b4, #ff7f0e); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .feature {{ background: white; margin: 15px 0; padding: 20px; border-radius: 8px; border-left: 4px solid #1f77b4; }}
                    .button {{ display: inline-block; background: #1f77b4; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📈 Welcome to {self.app_name}!</h1>
                        <p>Your journey to smarter trading starts here</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hello {username}! 👋</h2>
                        <p>Thank you for joining our trading community! We're excited to help you make informed investment decisions with our comprehensive stock analysis tools.</p>
                        
                        <h3>🚀 Getting Started Guide:</h3>
                        
                        <div class="feature">
                            <h4>📊 Stock Analysis</h4>
                            <p>Enter any stock ticker (e.g., AAPL, MSFT, GOOGL) to get comprehensive technical analysis including:</p>
                            <ul>
                                <li><strong>Moving Averages:</strong> SMA, EMA for trend analysis</li>
                                <li><strong>MACD:</strong> Momentum and trend changes</li>
                                <li><strong>Bollinger Bands:</strong> Volatility and support/resistance</li>
                                <li><strong>RSI:</strong> Overbought/oversold conditions</li>
                                <li><strong>SuperTrend:</strong> Trend following indicator</li>
                            </ul>
                        </div>
                        
                        <div class="feature">
                            <h4>🔥 Popular Stocks</h4>
                            <p>Discover trending stocks that other users are analyzing. Click on any popular stock to instantly analyze it!</p>
                        </div>
                        
                        <div class="feature">
                            <h4>⭐ Favorites</h4>
                            <p>Save your favorite stocks for quick access. Add stocks to your favorites list for easy monitoring.</p>
                        </div>
                        
                        <div class="feature">
                            <h4>📈 Interactive Charts</h4>
                            <p>Explore beautiful, interactive charts powered by Plotly. Zoom, pan, and analyze price movements in detail.</p>
                        </div>
                        
                        <h3>💡 Pro Tips:</h3>
                        <ul>
                            <li>Start with well-known stocks like AAPL, MSFT, or GOOGL</li>
                            <li>Try different date ranges (1 month, 3 months, 1 year) for different perspectives</li>
                            <li>Use the popular stocks section to discover trending opportunities</li>
                            <li>Check both US stocks (AAPL) and Indian stocks (ITC.NS, RELIANCE.NS)</li>
                        </ul>
                        
                        <p style="text-align: center;">
                            <a href="https://your-app-name.streamlit.app" class="button">Start Analyzing Stocks</a>
                        </p>
                        
                        <h3>🔒 Security Note:</h3>
                        <p>Your account is secured with industry-standard encryption. Never share your login credentials with anyone.</p>
                    </div>
                    
                    <div class="footer">
                        <p>Happy Trading! 📈</p>
                        <p><strong>{self.app_name} Team</strong></p>
                        <p>This is an automated message. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Welcome to {self.app_name}!
            
            Hello {username}!
            
            Thank you for joining our trading community! We're excited to help you make informed investment decisions.
            
            GETTING STARTED:
            
            1. STOCK ANALYSIS
               - Enter any stock ticker (AAPL, MSFT, GOOGL)
               - Get comprehensive technical analysis
               - View moving averages, MACD, Bollinger Bands, RSI, SuperTrend
            
            2. POPULAR STOCKS
               - Discover trending stocks
               - Click to instantly analyze
            
            3. FAVORITES
               - Save your favorite stocks
               - Quick access for monitoring
            
            4. INTERACTIVE CHARTS
               - Beautiful Plotly charts
               - Zoom, pan, analyze price movements
            
            PRO TIPS:
            - Start with AAPL, MSFT, GOOGL
            - Try different date ranges
            - Check both US and Indian stocks (ITC.NS, RELIANCE.NS)
            
            Start analyzing: https://your-app-name.streamlit.app
            
            Happy Trading!
            {self.app_name} Team
            """
            
            self._send_email(user_email, subject, html_body, text_body)
            logger.info(f"Welcome email sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user_email}: {e}")
            return False
    
    def send_password_reset_email(self, user_email, username, reset_token):
        """Send password reset email."""
        try:
            subject = f"Password Reset - {self.app_name}"
            
            # In a real app, you'd include the reset link with the token
            reset_link = f"https://your-app-name.streamlit.app?reset_token={reset_token}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #dc3545; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #dc3545; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔒 Password Reset Request</h1>
                        <p>{self.app_name}</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hello {username}!</h2>
                        <p>We received a request to reset your password for your {self.app_name} account.</p>
                        
                        <p style="text-align: center;">
                            <a href="{reset_link}" class="button">Reset My Password</a>
                        </p>
                        
                        <div class="warning">
                            <strong>⚠️ Important Security Information:</strong>
                            <ul>
                                <li>This link will expire in 1 hour for security reasons</li>
                                <li>If you didn't request this reset, please ignore this email</li>
                                <li>Your password will remain unchanged until you click the link above</li>
                            </ul>
                        </div>
                        
                        <p><strong>Reset Token:</strong> <code>{reset_token}</code></p>
                        <p><em>You can also manually enter this token in the app if the link doesn't work.</em></p>
                        
                        <h3>Need Help?</h3>
                        <p>If you're having trouble resetting your password, please contact our support team.</p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated security message from {self.app_name}</p>
                        <p>Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Password Reset Request - {self.app_name}
            
            Hello {username}!
            
            We received a request to reset your password for your {self.app_name} account.
            
            Reset your password: {reset_link}
            
            Reset Token: {reset_token}
            (You can manually enter this token in the app)
            
            IMPORTANT:
            - This link expires in 1 hour
            - If you didn't request this, please ignore this email
            - Your password remains unchanged until you reset it
            
            Need help? Contact our support team.
            
            {self.app_name} Security Team
            """
            
            self._send_email(user_email, subject, html_body, text_body)
            logger.info(f"Password reset email sent to {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user_email}: {e}")
            return False
    
    def _send_email(self, to_email, subject, html_body, text_body):
        """Send email using SMTP."""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email_address
            message["To"] = to_email
            
            # Create text and HTML parts
            text_part = MIMEText(text_body, "plain")
            html_part = MIMEText(html_body, "html")
            
            # Add parts to message
            message.attach(text_part)
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            raise

# Global email service instance
email_service = EmailService()

def get_email_service():
    """Get the global email service instance."""
    return email_service
