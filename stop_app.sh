#!/bin/bash

# Stop Streamlit Trading Simulator
echo "🛑 Stopping Streamlit Trading Simulator"
echo "======================================="

# Stop Streamlit process
if [ -f "streamlit.pid" ]; then
    STREAMLIT_PID=$(cat streamlit.pid)
    if ps -p $STREAMLIT_PID > /dev/null; then
        echo "📊 Stopping Streamlit app (PID: $STREAMLIT_PID)..."
        kill $STREAMLIT_PID
        rm streamlit.pid
    else
        echo "📊 Streamlit app not running"
    fi
else
    echo "📊 No Streamlit PID file found"
fi

# Stop keep-alive process
if [ -f "keep_alive.pid" ]; then
    KEEP_ALIVE_PID=$(cat keep_alive.pid)
    if ps -p $KEEP_ALIVE_PID > /dev/null; then
        echo "⏰ Stopping keep-alive service (PID: $KEEP_ALIVE_PID)..."
        kill $KEEP_ALIVE_PID
        rm keep_alive.pid
    else
        echo "⏰ Keep-alive service not running"
    fi
else
    echo "⏰ No keep-alive PID file found"
fi

# Kill any remaining processes
echo "🧹 Cleaning up any remaining processes..."
pkill -f "streamlit run trading_simulator.py"
pkill -f "keep_alive.py"

echo "✅ All processes stopped"
echo "💾 Your data is safely stored in the data/ directory"
