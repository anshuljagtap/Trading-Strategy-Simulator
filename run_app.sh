#!/bin/bash

# Stock Market Analysis Launcher
echo "🚀 Starting Stock Market Analysis..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/lib/python*/site-packages/streamlit" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo "🌐 Launching application..."
echo "📱 Open your browser and go to: http://localhost:8511"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""

streamlit run trading_simulator.py --server.port=8511 