#!/bin/bash

# Streamlit Trading Simulator - Startup Script
# This script starts the Streamlit app with keep-alive and data persistence

echo "🚀 Starting Streamlit Trading Simulator"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit, yfinance, pandas, numpy, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

# Create data directory if it doesn't exist
mkdir -p data
mkdir -p backups

# Start the Streamlit app in the background
echo "🌐 Starting Streamlit app..."
streamlit run trading_simulator.py --server.port 8501 --server.headless true &

# Get the PID of the Streamlit process
STREAMLIT_PID=$!
echo "📊 Streamlit app started with PID: $STREAMLIT_PID"

# Wait a moment for the app to start
sleep 5

# Start the keep-alive service
echo "🔄 Starting keep-alive service..."
python keep_alive.py &

# Get the PID of the keep-alive process
KEEP_ALIVE_PID=$!
echo "⏰ Keep-alive service started with PID: $KEEP_ALIVE_PID"

# Save PIDs to file for easy cleanup
echo $STREAMLIT_PID > streamlit.pid
echo $KEEP_ALIVE_PID > keep_alive.pid

echo ""
echo "✅ Trading Simulator is now running!"
echo "🌐 App URL: http://localhost:8501"
echo "📝 Logs: keep_alive.log"
echo "💾 Data: data/ directory"
echo ""
echo "To stop the app, run: ./stop_app.sh"
echo "To view logs: tail -f keep_alive.log"
echo ""

# Keep the script running
wait
