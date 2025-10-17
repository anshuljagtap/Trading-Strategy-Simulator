# 📈 Streamlit Trading Simulator

A comprehensive stock market analysis tool with real-time data, technical indicators, and persistent user data.

## 🚀 Features

- **🔐 User Authentication** - Secure login and registration system
- **📊 Real-time Stock Analysis** with Yahoo Finance data
- **Technical Indicators**: MACD, Bollinger Bands, RSI, SMA, EMA, SuperTrend
- **Interactive Charts** with Plotly
- **User Data Persistence** - Stats and analysis history are saved
- **Keep-Alive System** - App stays running and doesn't sleep
- **Automatic Backups** - Data is backed up regularly
- **Comprehensive Logging** - All activity is logged
- **User Statistics** - Track individual user analysis counts
- **Popular Stocks Tracking** - See the most searched stocks on the platform

## 🛠️ Setup

### Quick Start

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start the application:**
   ```bash
   ./run_app.sh
   ```

3. **Access the app:**
   - Open your browser to: `http://localhost:8501`

### Manual Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


3. **Run the app:**
   ```bash
   streamlit run trading_simulator.py
   ```

## 📊 Usage

### Authentication
- **Login**: Use your username and password to access the app
- **Register**: Create a new account with username, email, and password
- **Demo User**: Use `demo` / `demo123` for testing

### Stock Analysis
- Enter a stock ticker (e.g., AAPL, MSFT, GOOGL)
- Select date range for analysis
- View comprehensive technical analysis
- Get buy/sell recommendations
- Your analysis count is automatically tracked
- Popular stocks are displayed based on search frequency

### Data Persistence
- All user interactions are automatically saved
- Analysis history is preserved
- User statistics are maintained
- Data is backed up regularly

## 🔧 Management

### Start the App
```bash
./run_app.sh
```

### Stop the App
```bash
./stop_app.sh
```

### View Logs
```bash
tail -f keep_alive.log
```

### Data Location
- **User Data**: `data/users.json`
- **Statistics**: `data/stats.json`
- **Analysis History**: `data/analysis_history.json`
- **Stock Search Stats**: `data/stock_stats.json`
- **Backups**: `backups/` directory

## 🛡️ Keep-Alive System

The app includes an automatic keep-alive system that:
- Sends periodic pings to prevent the app from sleeping
- Logs all activity
- Automatically restarts if the app becomes unresponsive
- Runs every 5 minutes by default

## 💾 Data Persistence

Your data is automatically saved and includes:
- **User Information**: Sign-ups and user counts
- **Analysis History**: All stock analyses performed
- **Statistics**: App usage statistics
- **Session Data**: Current session information

## 🔄 Backup System

Automatic backups are created:
- Daily backups of all data files
- Timestamped backup folders
- Automatic cleanup of old backups (30+ days)
- Manual backup creation available

## 📝 Logging

Comprehensive logging includes:
- Keep-alive ping status
- Data save/load operations
- Error tracking
- Performance metrics

## 🚨 Troubleshooting

### App Won't Start
1. Check if port 8501 is available
2. Ensure all dependencies are installed
3. Check the logs: `tail -f keep_alive.log`

### Data Loss
1. Check the `data/` directory
2. Restore from backups in `backups/` directory
3. Check logs for error messages

### Keep-Alive Issues
1. Check if the keep-alive service is running
2. Verify the app URL is correct
3. Check network connectivity

## 📁 File Structure

```
├── trading_simulator.py    # Main Streamlit application
├── keep_alive.py          # Keep-alive service
├── data_persistence.py    # Data persistence module
├── run_app.sh            # Start script
├── stop_app.sh           # Stop script
├── setup.sh              # Setup script
├── requirements.txt      # Python dependencies
├── data/                 # Data storage directory
├── backups/              # Backup directory
└── logs/                 # Log files
```

## 🔧 Configuration

### Environment Variables
- `STREAMLIT_URL`: URL of the Streamlit app (default: http://localhost:8501)
- `KEEP_ALIVE_INTERVAL`: Ping interval in seconds (default: 300)

### Streamlit Configuration
The app uses `.streamlit/config.toml` for configuration:
- Headless mode enabled
- CORS disabled for local development
- Custom theme colors

## 📈 Technical Indicators

The app analyzes stocks using:
- **Moving Averages**: SMA, EMA
- **Momentum**: MACD, RSI
- **Volatility**: Bollinger Bands
- **Trend**: SuperTrend
- **Support/Resistance**: Pivot Points
- **Volume Analysis**: Volume trends

## 🎯 Recommendations

The app provides:
- **Buy/Sell/Hold** recommendations
- **Confidence levels** (High/Medium/Low)
- **Risk assessment** with volatility metrics
- **Support and resistance** levels
- **Detailed reasoning** for each recommendation

## 📞 Support

For issues or questions:
1. Check the logs first
2. Verify all dependencies are installed
3. Ensure the virtual environment is activated
4. Check if ports are available

---

**Happy Trading! 📈**
