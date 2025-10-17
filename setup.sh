#!/bin/bash

# Setup script for Streamlit Trading Simulator
echo "🔧 Setting up Streamlit Trading Simulator"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Install additional packages for keep-alive
echo "🔧 Installing additional packages..."
pip install requests watchdog

# Make scripts executable
echo "🔐 Making scripts executable..."
chmod +x run_app.sh
chmod +x stop_app.sh

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p backups
mkdir -p logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the app: ./run_app.sh"
echo "🛑 To stop the app: ./stop_app.sh"
echo "📊 App will be available at: http://localhost:8501"
echo ""
echo "💡 The app will now:"
echo "   - Stay alive with automatic keep-alive pings"
echo "   - Save all user data and stats persistently"
echo "   - Create automatic backups"
echo "   - Log all activity"
