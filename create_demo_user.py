#!/usr/bin/env python3
"""
Create a demo user for testing the authentication system
"""

from auth import auth_manager

def create_demo_user():
    """Create a demo user for testing."""
    username = "demo"
    email = "demo@trading.com"
    password = "demo123"
    
    success, message = auth_manager.register_user(username, email, password)
    
    if success:
        print(f"✅ Demo user created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"\nYou can now login with these credentials.")
    else:
        print(f"❌ Failed to create demo user: {message}")

if __name__ == "__main__":
    create_demo_user()
