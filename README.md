# 📈 Trading Strategy Simulator

A comprehensive stock market analysis tool built with Streamlit that provides technical analysis, trading signals, and weighted recommendations.

## ✨ Features

- **📊 Technical Indicators**: SMA, EMA, MACD, Bollinger Bands, SuperTrend, Volume Analysis
- **🎯 Weighted Recommendations**: AI-powered buy/sell/hold signals with confidence levels
- **⭐ Favorites Management**: Save and manage your favorite stocks
- **📈 Interactive Charts**: Beautiful Plotly visualizations
- **⚡ Quick Actions**: One-click analysis for popular stocks
- **📱 Responsive Design**: Works on desktop and mobile

## 🚀 Quick Deploy (Recommended)

### Option 1: Streamlit Cloud (FREE)
1. **Run the deployment script:**
   ```bash
   ./deploy.sh
   ```
2. **Follow the prompts** to create a GitHub repository
3. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `trading_simulator.py`
   - Click "Deploy!"

**Your app will be live at:** `https://your-app-name.streamlit.app`

### Option 2: Local Network Sharing
```bash
# Run with network access
streamlit run trading_simulator.py --server.address=0.0.0.0 --server.port=8501
```
Others can access: `http://YOUR_IP:8501`

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/trading-strategy-simulator.git
   cd trading-strategy-simulator
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run trading_simulator.py
   ```

5. **Open in browser:**
   ```
   http://localhost:8501
   ```

## 📊 Technical Indicators

### Moving Averages
- **50-Day SMA**: Short-term trend analysis
- **200-Day SMA**: Long-term trend analysis
- **Golden Cross/Death Cross**: Trend reversal signals

### Momentum Indicators
- **MACD**: Momentum and trend changes
- **Signal Line**: MACD confirmation
- **SuperTrend**: Trend following with stop-loss

### Volatility Indicators
- **Bollinger Bands**: Price volatility and overbought/oversold levels
- **Volume Trend**: Trading volume analysis

### Support/Resistance
- **Pivot Points**: Key support and resistance levels
- **R1/S1**: Dynamic support and resistance

## 🎯 Recommendation System

The app uses a **weighted scoring system** with 7 technical indicators:

- **SuperTrend (25%)**: Highest weight for trend analysis
- **Moving Averages (20%)**: SMA and EMA analysis
- **MACD (20%)**: Momentum analysis
- **EMA (15%)**: Exponential moving averages
- **Bollinger Bands (10%)**: Volatility analysis
- **Pivot Points (10%)**: Support/resistance levels
- **Volume (5%)**: Volume confirmation

### Recommendation Levels
- 🟢 **STRONG BUY** (≥75%): High confidence buy signal
- 🟡 **BUY** (≥65%): Moderate confidence buy signal
- 🟠 **HOLD** (≥45%): Wait for clearer signals
- 🔴 **SELL** (≥35%): Consider selling
- 🔴 **STRONG SELL** (<35%): High confidence sell signal

## ⭐ Favorites Management

- **Add Favorites**: Type a stock ticker and click "+"
- **Quick Access**: Click on any favorite to analyze instantly
- **Remove Favorites**: Click "❌" to remove from favorites
- **Auto-Add**: "⭐ Add to Favorites" button for current stock
- **Clear All**: "🗑️ Clear All Favorites" to start fresh

## 🌐 Supported Stocks

The app supports stocks from major exchanges:
- **US Stocks**: AAPL, MSFT, GOOGL, TSLA, AMZN, etc.
- **Indian Stocks**: ITC.NS, RELIANCE.NS, TCS.NS, etc.
- **Global Stocks**: Any ticker supported by Yahoo Finance

## 🔧 Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: Usage statistics

### Customization
- Modify `trading_simulator.py` to add new indicators
- Update weights in `generate_recommendation()` function
- Add new stocks to `popular_stocks` list

## 📱 Usage

1. **Enter Stock Ticker**: Type a stock symbol (e.g., AAPL, MSFT)
2. **Select Date Range**: Choose analysis period
3. **View Analysis**: Explore charts and indicators
4. **Check Recommendations**: See weighted buy/sell signals
5. **Manage Favorites**: Save stocks for quick access

## 🚨 Important Notes

- **Data Source**: Yahoo Finance API (free tier)
- **Rate Limits**: Respect API usage limits
- **Educational Purpose**: Not financial advice
- **Real-time Data**: Delayed by 15-20 minutes

## 🐛 Troubleshooting

### Common Issues
1. **"No data found"**: Check ticker symbol spelling
2. **Slow loading**: Reduce date range or check internet
3. **Chart issues**: Refresh page or try different stock

### Performance Tips
- Use shorter date ranges for faster loading
- Clear browser cache if charts don't load
- Check internet connection for data fetching

## 📈 Future Enhancements

- [ ] Real-time data feeds
- [ ] Portfolio tracking
- [ ] Backtesting capabilities
- [ ] More technical indicators
- [ ] Mobile app version
- [ ] User authentication
- [ ] Custom alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please do your own research before making investment decisions.

## 📞 Support

- **Issues**: Create a GitHub issue
- **Questions**: Check the documentation
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

---

**⚠️ Disclaimer**: This tool is for educational purposes only. Not financial advice. Always do your own research and consult with financial advisors before making investment decisions.

**Happy Trading! 📈💰** 