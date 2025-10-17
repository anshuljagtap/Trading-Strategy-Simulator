#!/usr/bin/env python3
"""
Basic Trading Simulator without Email Functionality
This version removes email dependencies to ensure successful deployment
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists."""
        os.makedirs("data", exist_ok=True)
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """Load users from JSON file."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            return {}
    
    def save_users(self, users: Dict):
        """Save users to JSON file."""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Register a new user."""
        users = self.load_users()
        
        if username in users:
            return False, "Username already exists"
        
        # Check if email is already registered
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
        logger.info(f"New user registered: {username}")
        return True, "Registration successful!"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate a user."""
        users = self.load_users()
        
        if username not in users:
            return False, "Invalid username or password", None
        
        user_data = users[username]
        hashed_password = self.hash_password(password)
        
        if user_data['password'] != hashed_password:
            return False, "Invalid username or password", None
        
        # Update login info
        user_data['last_login'] = datetime.now().isoformat()
        user_data['login_count'] = user_data.get('login_count', 0) + 1
        self.save_users(users)
        
        logger.info(f"User authenticated: {username}")
        return True, "Login successful!", user_data

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
    
    # Display user stats
    st.markdown("---")
    users = auth_manager.load_users()
    total_users = len(users)
    total_analyses = sum(user.get('analyses_count', 0) for user in users.values())
    active_users = len([user for user in users.values() if user.get('login_count', 0) > 0])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("Total Analyses", total_analyses)
    with col3:
        st.metric("Active Users", active_users)

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

def main():
    """Main application function."""
    # Authentication
    if not main_auth():
        return
    
    # Main app content
    st.title("📈 Trading Strategy Simulator")
    st.markdown("---")
    
    # Welcome message
    st.success(f"Welcome back, {st.session_state.username}! 🎉")
    
    # Sidebar
    st.sidebar.header("📊 Analysis Settings")
    
    # Stock input
    ticker = st.sidebar.text_input("Stock Ticker", value="AAPL", placeholder="Enter stock symbol (e.g., AAPL)")
    
    # Date range
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Analysis button
    if st.sidebar.button("Analyze Stock", width='stretch'):
        if ticker:
            try:
                # Fetch data
                stock = yf.Ticker(ticker)
                data = stock.history(start=start_date, end=end_date)
                
                if data.empty:
                    st.error(f"No data found for {ticker}")
                    return
                
                # Basic analysis
                st.header(f"📊 Analysis for {ticker}")
                
                # Price chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
                fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, width='stretch')
                
                # Basic statistics
                st.subheader("📈 Basic Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Price", f"${data['Close'].iloc[-1]:.2f}")
                with col2:
                    st.metric("52-Week High", f"${data['High'].max():.2f}")
                with col3:
                    st.metric("52-Week Low", f"${data['Low'].min():.2f}")
                with col4:
                    st.metric("Volume", f"{data['Volume'].iloc[-1]:,}")
                
                # Update user analysis count
                users = auth_manager.load_users()
                if st.session_state.username in users:
                    users[st.session_state.username]['analyses_count'] = users[st.session_state.username].get('analyses_count', 0) + 1
                    auth_manager.save_users(users)
                
                st.success("Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {str(e)}")
        else:
            st.error("Please enter a stock ticker")

if __name__ == "__main__":
    main()
