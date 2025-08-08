@echo off
echo 🚀 Starting Stock Market Analysis...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\Lib\site-packages\streamlit" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
echo 🌐 Launching application...
echo 📱 Open your browser and go to: http://localhost:8511
echo ⏹️  Press Ctrl+C to stop the application
echo.

streamlit run trading_simulator.py --server.port=8511

pause 