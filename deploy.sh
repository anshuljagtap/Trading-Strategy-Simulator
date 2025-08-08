#!/bin/bash

# 🚀 Trading Strategy Simulator Deployment Script
# This script helps you deploy your app to Streamlit Cloud

echo "🚀 Starting deployment process..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Trading Strategy Simulator"
    echo "✅ Git repository initialized"
else
    echo "📁 Git repository already exists"
fi

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🌐 Please create a GitHub repository and run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/trading-strategy-simulator.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "📋 Then follow these steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select your repository"
    echo "5. Set main file path to: trading_simulator.py"
    echo "6. Click 'Deploy!'"
else
    echo "🌐 Remote repository found"
    echo "📤 Pushing to GitHub..."
    git add .
    git commit -m "Update: Trading Strategy Simulator"
    git push origin main
    echo "✅ Code pushed to GitHub"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select your repository"
    echo "5. Set main file path to: trading_simulator.py"
    echo "6. Click 'Deploy!'"
fi

echo ""
echo "🎉 Deployment script completed!"
echo "📖 For more options, see DEPLOYMENT_GUIDE.md" 