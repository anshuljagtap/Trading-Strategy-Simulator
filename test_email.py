#!/usr/bin/env python3
"""
Test Email Functionality for Trading Simulator
Run this to test email configuration and functionality
"""

import os
import sys
from email_service import get_email_service

def test_email_config():
    """Test email configuration."""
    print("🧪 Testing Email Configuration")
    print("=" * 40)
    
    # Check environment variables
    required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set up email configuration first:")
        print("python setup_email.py")
        return False
    
    print("✅ All environment variables are set")
    
    # Test email service initialization
    try:
        email_service = get_email_service()
        if email_service:
            print("✅ Email service initialized successfully")
            return True
        else:
            print("❌ Failed to initialize email service")
            return False
    except Exception as e:
        print(f"❌ Error initializing email service: {e}")
        return False

def test_welcome_email():
    """Test welcome email functionality."""
    print("\n📧 Testing Welcome Email")
    print("-" * 30)
    
    test_email = input("Enter test email address (or press Enter to skip): ").strip()
    
    if not test_email:
        print("⏭️  Skipping welcome email test")
        return True
    
    try:
        email_service = get_email_service()
        if email_service:
            print(f"Sending test welcome email to {test_email}...")
            success = email_service.send_welcome_email(test_email, "TestUser")
            
            if success:
                print("✅ Welcome email sent successfully!")
                print("Check your inbox for the welcome email.")
                return True
            else:
                print("❌ Failed to send welcome email")
                return False
        else:
            print("❌ Email service not available")
            return False
    except Exception as e:
        print(f"❌ Error sending welcome email: {e}")
        return False

def test_password_reset_email():
    """Test password reset email functionality."""
    print("\n🔑 Testing Password Reset Email")
    print("-" * 35)
    
    test_email = input("Enter test email address (or press Enter to skip): ").strip()
    
    if not test_email:
        print("⏭️  Skipping password reset email test")
        return True
    
    try:
        email_service = get_email_service()
        if email_service:
            # Generate a test token
            test_token = email_service.generate_reset_token()
            print(f"Sending test password reset email to {test_email}...")
            success = email_service.send_password_reset_email(test_email, "TestUser", test_token)
            
            if success:
                print("✅ Password reset email sent successfully!")
                print("Check your inbox for the reset email.")
                print(f"Test token: {test_token}")
                return True
            else:
                print("❌ Failed to send password reset email")
                return False
        else:
            print("❌ Email service not available")
            return False
    except Exception as e:
        print(f"❌ Error sending password reset email: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Trading Simulator - Email Functionality Test")
    print("=" * 50)
    print()
    
    # Test 1: Configuration
    config_ok = test_email_config()
    
    if not config_ok:
        print("\n❌ Email configuration test failed!")
        print("Please run: python setup_email.py")
        return
    
    # Test 2: Welcome Email
    welcome_ok = test_welcome_email()
    
    # Test 3: Password Reset Email
    reset_ok = test_password_reset_email()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Welcome Email: {'✅ PASS' if welcome_ok else '❌ FAIL'}")
    print(f"Reset Email:   {'✅ PASS' if reset_ok else '❌ FAIL'}")
    
    if config_ok and welcome_ok and reset_ok:
        print("\n🎉 All email tests passed!")
        print("Your email functionality is ready to use!")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
    
    print("\nNext steps:")
    print("1. Run your Streamlit app: streamlit run trading_simulator.py")
    print("2. Test registration to receive welcome emails")
    print("3. Test forgot password functionality")

if __name__ == "__main__":
    main()
