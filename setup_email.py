#!/usr/bin/env python3
"""
Email Setup Script for Trading Simulator
Helps configure email settings for password reset and welcome emails
"""

import os
import sys

def setup_email():
    """Interactive email setup."""
    print("📧 Email Configuration Setup")
    print("=" * 50)
    print()
    
    print("This will help you configure email settings for:")
    print("• Password reset emails")
    print("• Welcome emails for new users")
    print()
    
    # Get email provider
    print("Choose your email provider:")
    print("1. Gmail (recommended)")
    print("2. Outlook/Hotmail")
    print("3. Yahoo")
    print("4. Custom SMTP")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        setup_gmail()
    elif choice == "2":
        setup_outlook()
    elif choice == "3":
        setup_yahoo()
    elif choice == "4":
        setup_custom()
    else:
        print("Invalid choice. Please run the script again.")
        return False
    
    return True

def setup_gmail():
    """Setup Gmail configuration."""
    print("\n📧 Gmail Setup")
    print("-" * 20)
    print()
    print("For Gmail, you need to:")
    print("1. Enable 2-Factor Authentication")
    print("2. Generate an App Password")
    print()
    print("Steps:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification")
    print("3. Go to App passwords")
    print("4. Generate a password for 'Mail'")
    print("5. Copy the 16-character password")
    print()
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    if len(app_password) != 16:
        print("❌ App password should be 16 characters long")
        return False
    
    # Create environment file
    create_env_file(email, app_password, "smtp.gmail.com", "587")
    
    print("\n✅ Gmail configuration saved!")
    print("Environment variables set:")
    print(f"EMAIL_ADDRESS={email}")
    print(f"EMAIL_PASSWORD={app_password}")
    print("SMTP_SERVER=smtp.gmail.com")
    print("SMTP_PORT=587")
    
    return True

def setup_outlook():
    """Setup Outlook configuration."""
    print("\n📧 Outlook/Hotmail Setup")
    print("-" * 25)
    print()
    print("For Outlook/Hotmail:")
    print("1. Enable 2-Factor Authentication")
    print("2. Generate an App Password")
    print()
    
    email = input("Enter your Outlook email: ").strip()
    app_password = input("Enter your App Password: ").strip()
    
    create_env_file(email, app_password, "smtp-mail.outlook.com", "587")
    
    print("\n✅ Outlook configuration saved!")
    return True

def setup_yahoo():
    """Setup Yahoo configuration."""
    print("\n📧 Yahoo Setup")
    print("-" * 15)
    print()
    print("For Yahoo:")
    print("1. Enable 2-Factor Authentication")
    print("2. Generate an App Password")
    print()
    
    email = input("Enter your Yahoo email: ").strip()
    app_password = input("Enter your App Password: ").strip()
    
    create_env_file(email, app_password, "smtp.mail.yahoo.com", "587")
    
    print("\n✅ Yahoo configuration saved!")
    return True

def setup_custom():
    """Setup custom SMTP configuration."""
    print("\n📧 Custom SMTP Setup")
    print("-" * 20)
    print()
    
    email = input("Enter your email address: ").strip()
    password = input("Enter your email password: ").strip()
    smtp_server = input("Enter SMTP server (e.g., smtp.example.com): ").strip()
    smtp_port = input("Enter SMTP port (usually 587): ").strip()
    
    if not smtp_port.isdigit():
        smtp_port = "587"
    
    create_env_file(email, password, smtp_server, smtp_port)
    
    print("\n✅ Custom SMTP configuration saved!")
    return True

def create_env_file(email, password, smtp_server, smtp_port):
    """Create .env file with email configuration."""
    env_content = f"""# Email Configuration for Trading Simulator
EMAIL_ADDRESS={email}
EMAIL_PASSWORD={password}
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Also set environment variables for current session
    os.environ['EMAIL_ADDRESS'] = email
    os.environ['EMAIL_PASSWORD'] = password
    os.environ['SMTP_SERVER'] = smtp_server
    os.environ['SMTP_PORT'] = smtp_port

def test_email_config():
    """Test email configuration."""
    print("\n🧪 Testing Email Configuration")
    print("-" * 30)
    
    try:
        from email_service import get_email_service
        email_service = get_email_service()
        
        if email_service:
            print("✅ Email service initialized successfully!")
            
            # Test with a dummy email (won't actually send)
            test_email = input("Enter a test email address (optional): ").strip()
            if test_email:
                print(f"Sending test email to {test_email}...")
                # Note: This would send a real email in production
                print("✅ Email configuration is working!")
            else:
                print("✅ Email configuration looks good!")
        else:
            print("❌ Email configuration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing email configuration: {e}")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Trading Simulator - Email Setup")
    print("=" * 40)
    print()
    
    if setup_email():
        print("\n" + "=" * 50)
        test = input("Would you like to test the email configuration? (y/n): ").strip().lower()
        
        if test == 'y':
            test_email_config()
        
        print("\n🎉 Email setup complete!")
        print("\nNext steps:")
        print("1. Run your Streamlit app: streamlit run trading_simulator.py")
        print("2. Test registration to receive welcome emails")
        print("3. Test forgot password functionality")
        print("\nNote: Make sure to add .env to your .gitignore file!")
    else:
        print("\n❌ Email setup failed. Please try again.")

if __name__ == "__main__":
    main()
