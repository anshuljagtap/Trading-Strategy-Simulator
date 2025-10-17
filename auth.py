#!/usr/bin/env python3
"""
Authentication module for Streamlit Trading Simulator
Handles user login, registration, and session management
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
import logging
from email_service import get_email_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, users_file="data/users.json"):
        """
        Initialize the authentication manager.
        
        Args:
            users_file (str): Path to the users JSON file
        """
        self.users_file = users_file
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Create users file and data directory if they don't exist."""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
            logger.info(f"Created users file: {self.users_file}")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """Load users from the JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_users(self, users: Dict):
        """Save users to the JSON file."""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            logger.info(f"Saved {len(users)} users to {self.users_file}")
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Plain text password
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        users = self.load_users()
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists"
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email') == email:
                return False, "Email already registered"
        
        # Create new user
        user_id = str(len(users) + 1)
        hashed_password = self.hash_password(password)
        
        users[username] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'login_count': 0,
            'subscription_tier': 'free',
            'analyses_count': 0,
            'favorites': []
        }
        
        self.save_users(users)
        
        # Send welcome email
        try:
            self.send_welcome_email(username, email)
        except Exception as e:
            logger.warning(f"Failed to send welcome email to {username}: {e}")
        
        logger.info(f"New user registered: {username}")
        return True, "Registration successful! Check your email for a welcome message and login guide."
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate a user.
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        users = self.load_users()
        
        if username not in users:
            return False, "Invalid username or password", None
        
        user_data = users[username]
        hashed_password = self.hash_password(password)
        
        if user_data['password'] != hashed_password:
            return False, "Invalid username or password", None
        
        # Update last login and login count
        user_data['last_login'] = datetime.now().isoformat()
        user_data['login_count'] = user_data.get('login_count', 0) + 1
        
        self.save_users(users)
        logger.info(f"User authenticated: {username}")
        
        # Return user data without password
        user_info = {k: v for k, v in user_data.items() if k != 'password'}
        return True, "Login successful!", user_info
    
    def get_user_stats(self) -> Dict:
        """Get overall user statistics."""
        users = self.load_users()
        
        total_users = len(users)
        total_analyses = sum(user.get('analyses_count', 0) for user in users.values())
        active_users = sum(1 for user in users.values() 
                          if user.get('last_login') and 
                          datetime.fromisoformat(user['last_login']) > datetime.now() - timedelta(days=30))
        
        return {
            'total_users': total_users,
            'total_analyses': total_analyses,
            'active_users': active_users,
            'last_updated': datetime.now().isoformat()
        }
    
    def track_stock_search(self, ticker: str):
        """Track a stock search/analysis."""
        stats_file = os.path.join(os.path.dirname(self.users_file), "stock_stats.json")
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stock_stats = json.load(f)
            else:
                stock_stats = {}
            
            # Increment count for this ticker
            if ticker in stock_stats:
                stock_stats[ticker]['count'] += 1
                stock_stats[ticker]['last_searched'] = datetime.now().isoformat()
            else:
                stock_stats[ticker] = {
                    'count': 1,
                    'first_searched': datetime.now().isoformat(),
                    'last_searched': datetime.now().isoformat()
                }
            
            # Save updated stats
            with open(stats_file, 'w') as f:
                json.dump(stock_stats, f, indent=2)
                
            logger.info(f"Tracked stock search: {ticker}")
            
        except Exception as e:
            logger.error(f"Failed to track stock search: {e}")
    
    def get_popular_stocks(self, limit: int = 10) -> List[Dict]:
        """Get the most popular stocks by search count."""
        stats_file = os.path.join(os.path.dirname(self.users_file), "stock_stats.json")
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stock_stats = json.load(f)
                
                # Sort by count and return top stocks
                sorted_stocks = sorted(
                    stock_stats.items(), 
                    key=lambda x: x[1]['count'], 
                    reverse=True
                )
                
                return [
                    {
                        'ticker': ticker,
                        'count': data['count'],
                        'last_searched': data.get('last_searched', 'N/A')
                    }
                    for ticker, data in sorted_stocks[:limit]
                ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to get popular stocks: {e}")
            return []
    
    def increment_analysis_count(self, username: str):
        """Increment the analysis count for a user."""
        users = self.load_users()
        if username in users:
            users[username]['analyses_count'] = users[username].get('analyses_count', 0) + 1
            self.save_users(users)
    
    def request_password_reset(self, email: str) -> Tuple[bool, str]:
        """
        Request a password reset for a user.
        
        Args:
            email (str): User's email address
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        users = self.load_users()
        
        # Find user by email
        user_found = None
        for username, user_data in users.items():
            if user_data.get('email') == email:
                user_found = (username, user_data)
                break
        
        if not user_found:
            return False, "No account found with this email address"
        
        username, user_data = user_found
        
        # Generate reset token
        email_service = get_email_service()
        reset_token = email_service.generate_reset_token()
        
        # Store reset token with expiration
        reset_tokens_file = os.path.join(os.path.dirname(self.users_file), "reset_tokens.json")
        
        try:
            if os.path.exists(reset_tokens_file):
                with open(reset_tokens_file, 'r') as f:
                    reset_tokens = json.load(f)
            else:
                reset_tokens = {}
            
            # Store token with expiration (1 hour)
            reset_tokens[reset_token] = {
                'username': username,
                'email': email,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=1)).isoformat(),
                'used': False
            }
            
            with open(reset_tokens_file, 'w') as f:
                json.dump(reset_tokens, f, indent=2)
            
            # Send reset email
            if email_service.send_password_reset_email(email, username, reset_token):
                logger.info(f"Password reset requested for {username} ({email})")
                return True, "Password reset email sent! Check your inbox."
            else:
                return False, "Failed to send reset email. Please try again."
                
        except Exception as e:
            logger.error(f"Failed to process password reset request: {e}")
            return False, "An error occurred. Please try again."
    
    def reset_password_with_token(self, reset_token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset password using a reset token.
        
        Args:
            reset_token (str): Reset token from email
            new_password (str): New password
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        reset_tokens_file = os.path.join(os.path.dirname(self.users_file), "reset_tokens.json")
        
        try:
            if not os.path.exists(reset_tokens_file):
                return False, "Invalid reset token"
            
            with open(reset_tokens_file, 'r') as f:
                reset_tokens = json.load(f)
            
            if reset_token not in reset_tokens:
                return False, "Invalid reset token"
            
            token_data = reset_tokens[reset_token]
            
            # Check if token is expired
            expires_at = datetime.fromisoformat(token_data['expires_at'])
            if datetime.now() > expires_at:
                return False, "Reset token has expired. Please request a new one."
            
            # Check if token is already used
            if token_data['used']:
                return False, "Reset token has already been used. Please request a new one."
            
            # Update user's password
            users = self.load_users()
            username = token_data['username']
            
            if username not in users:
                return False, "User not found"
            
            # Hash new password
            hashed_password = self.hash_password(new_password)
            users[username]['password'] = hashed_password
            
            # Save updated users
            self.save_users(users)
            
            # Mark token as used
            reset_tokens[reset_token]['used'] = True
            with open(reset_tokens_file, 'w') as f:
                json.dump(reset_tokens, f, indent=2)
            
            logger.info(f"Password reset successful for {username}")
            return True, "Password reset successful! You can now login with your new password."
            
        except Exception as e:
            logger.error(f"Failed to reset password: {e}")
            return False, "An error occurred. Please try again."
    
    def send_welcome_email(self, username: str, email: str) -> bool:
        """Send welcome email to new user."""
        try:
            email_service = get_email_service()
            return email_service.send_welcome_email(email, username)
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False

# Global auth manager instance
auth_manager = AuthManager()

def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None

def login_page():
    """Display the login page."""
    st.title("🔐 Login to Trading Simulator")
    st.markdown("---")
    
    # Check for password reset token in URL parameters
    query_params = st.query_params
    reset_token = query_params.get('reset_token')
    
    if reset_token:
        # Show password reset form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.subheader("🔒 Reset Your Password")
            st.info("Enter your new password below.")
            
            with st.form("reset_password_form"):
                new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")
                confirm_password = st.text_input("Confirm New Password", type="password", placeholder="Confirm your new password")
                reset_button = st.form_submit_button("Reset Password", width='stretch')
                
                if reset_button:
                    if new_password and confirm_password:
                        if new_password == confirm_password:
                            success, message = auth_manager.reset_password_with_token(reset_token, new_password)
                            if success:
                                st.success(message)
                                st.info("You can now login with your new password.")
                                # Clear the reset token from URL
                                st.query_params.clear()
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please fill in all fields")
            
            st.markdown("---")
            st.markdown("**Remember your password?** [Login here](#login)")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_clicked = st.form_submit_button("Login", width='stretch')
            
            with col_register:
                register_clicked = st.form_submit_button("Register", width='stretch')
        
        if login_clicked:
            if username and password:
                success, message, user_data = auth_manager.authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_data = user_data
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
        
        if register_clicked:
            st.session_state.show_register = True
            st.rerun()
        
        # Forgot password section
        st.markdown("---")
        st.markdown("### 🔑 Forgot Your Password?")
        st.info("Enter your email address and we'll send you a password reset link.")
        
        with st.form("forgot_password_form"):
            reset_email = st.text_input("Email Address", placeholder="Enter your registered email", key="forgot_email")
            reset_button = st.form_submit_button("Send Reset Link", width='stretch')
            
            if reset_button:
                if reset_email:
                    success, message = auth_manager.request_password_reset(reset_email)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please enter your email address")
    
    # Display user stats
    st.markdown("---")
    stats = auth_manager.get_user_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", stats['total_users'])
    with col2:
        st.metric("Total Analyses", stats['total_analyses'])
    with col3:
        st.metric("Active Users", stats['active_users'])

def register_page():
    """Display the registration page."""
    st.title("📝 Create New Account")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Join the Trading Community!")
        
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            col_register, col_back = st.columns(2)
            
            with col_register:
                register_clicked = st.form_submit_button("Create Account", width='stretch')
            
            with col_back:
                back_clicked = st.form_submit_button("Back to Login", width='stretch')
        
        if register_clicked:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = auth_manager.register_user(username, email, password)
                    if success:
                        st.success(message)
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")
        
        if back_clicked:
            st.session_state.show_register = False
            st.rerun()

def logout():
    """Logout the current user."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.rerun()

def show_user_info():
    """Display user information in the sidebar."""
    if st.session_state.authenticated and st.session_state.user_data:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 User Info")
            st.write(f"**Username:** {st.session_state.username}")
            st.write(f"**Email:** {st.session_state.user_data.get('email', 'N/A')}")
            st.write(f"**Analyses:** {st.session_state.user_data.get('analyses_count', 0)}")
            st.write(f"**Member since:** {st.session_state.user_data.get('created_at', 'N/A')[:10]}")
            
            if st.button("Logout", width='stretch'):
                logout()

def require_auth(func):
    """Decorator to require authentication for a function."""
    def wrapper(*args, **kwargs):
        if not st.session_state.authenticated:
            st.error("Please login to access this feature")
            return None
        return func(*args, **kwargs)
    return wrapper

def main_auth():
    """Main authentication function."""
    init_session_state()
    
    if not st.session_state.authenticated:
        if st.session_state.get('show_register', False):
            register_page()
        else:
            login_page()
        return False
    
    show_user_info()
    return True
