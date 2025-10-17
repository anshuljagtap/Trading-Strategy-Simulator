import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import os
from auth import main_auth, auth_manager, require_auth

# Page configuration
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Simple user counter
def get_user_count():
    """Get total number of users who have signed up."""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
            return len(users)
    return 0

def increment_user_count():
    """Increment user count when someone signs up."""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    # Add a timestamp-based user entry
    timestamp = datetime.now().isoformat()
    users[f"user_{timestamp}"] = {
        "signup_date": timestamp
    }
    
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

# Fetching Data
def fetch_data(ticker, start_date, end_date):
    """Fetch stock data using yfinance."""
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
        if stock_data.empty:
            st.error(f"No data found for {ticker}. Please check the ticker symbol.")
            return None
        return stock_data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

# Preprocessing Data
def preprocess_data(stock_data):
    """Preprocess stock data by removing NaN values."""
    stock_data = stock_data.dropna()
    return stock_data

# Calculating Moving Averages
def calculate_moving_averages(stock_data):
    """Calculate SMA and EMA moving averages."""
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust=False).mean()
    stock_data['EMA_200'] = stock_data['Close'].ewm(span=200, adjust=False).mean()
    return stock_data

# Calculating MACD
def calculate_macd(stock_data):
    """Calculate MACD and Signal Line."""
    stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD'] = stock_data['EMA_12'] - stock_data['EMA_26']
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    return stock_data

# Calculating Bollinger Bands
def calculate_bollinger_bands(stock_data):
    """Calculate Bollinger Bands."""
    stock_data['20_day_SMA'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['20_day_std'] = stock_data['Close'].rolling(window=20).std()
    stock_data['Upper_Band'] = stock_data['20_day_SMA'] + (stock_data['20_day_std'] * 2)
    stock_data['Lower_Band'] = stock_data['20_day_SMA'] - (stock_data['20_day_std'] * 2)
    return stock_data

# Calculating Volume Trend
def volume_trend(stock_data):
    """Calculate volume trend."""
    stock_data['Volume_Trend'] = stock_data['Volume'].rolling(window=20).mean()
    return stock_data

# Calculating SuperTrend
def calculate_supertrend(stock_data, period=7, multiplier=3):
    """Calculate SuperTrend indicator."""
    try:
        # Calculate ATR as a Series
        atr = stock_data['High'].rolling(window=period).max() - stock_data['Low'].rolling(window=period).min()
        stock_data['ATR'] = atr
        
        # Calculate bands as Series
        typical_price = (stock_data['High'] + stock_data['Low']) / 2
        upper_band = typical_price + (multiplier * atr)
        lower_band = typical_price - (multiplier * atr)
        
        stock_data['Upper_Band_ST'] = upper_band
        stock_data['Lower_Band_ST'] = lower_band
        stock_data['SuperTrend'] = 0.0
        
        for i in range(1, len(stock_data)):
            try:
                # Get scalar values and handle NaN
                close_prev = stock_data['Close'].iloc[i-1]
                upper_band_prev = stock_data['Upper_Band_ST'].iloc[i-1]
                lower_band_prev = stock_data['Lower_Band_ST'].iloc[i-1]
                supertrend_prev = stock_data['SuperTrend'].iloc[i-1]
                
                # Check for NaN values
                if pd.isna(close_prev) or pd.isna(upper_band_prev) or pd.isna(lower_band_prev):
                    continue
                    
                if close_prev > upper_band_prev:
                    stock_data.loc[stock_data.index[i], 'SuperTrend'] = stock_data['Upper_Band_ST'].iloc[i]
                elif close_prev < lower_band_prev:
                    stock_data.loc[stock_data.index[i], 'SuperTrend'] = stock_data['Lower_Band_ST'].iloc[i]
                else:
                    stock_data.loc[stock_data.index[i], 'SuperTrend'] = supertrend_prev
            except (ValueError, TypeError, IndexError):
                # Skip problematic rows
                continue
        
        return stock_data
    except Exception as e:
        # If SuperTrend calculation fails, return original data with empty SuperTrend
        stock_data['SuperTrend'] = 0.0
        return stock_data

# Calculating Pivot Points
def calculate_pivot_points(stock_data):
    """Calculate pivot points."""
    try:
        # Calculate pivot as Series
        pivot = (stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 3
        stock_data['Pivot'] = pivot
        
        # Calculate R1 and S1 as Series
        r1 = 2 * pivot - stock_data['Low']
        s1 = 2 * pivot - stock_data['High']
        
        stock_data['R1'] = r1
        stock_data['S1'] = s1
        
        return stock_data
    except Exception as e:
        # If pivot calculation fails, return data with empty pivot columns
        stock_data['Pivot'] = 0.0
        stock_data['R1'] = 0.0
        stock_data['S1'] = 0.0
        return stock_data

# Calculating Buy/Sell Signals based on Trading Strategy
def trading_strategy(stock_data):
    """Calculate buy/sell signals based on trading strategy."""
    try:
        # Ensure all required columns exist
        required_columns = ['Close', 'SuperTrend', 'R1']
        for col in required_columns:
            if col not in stock_data.columns:
                stock_data[col] = 0.0
        
        # Calculate signals with NaN handling
        buy_condition = (stock_data['Close'] > stock_data['SuperTrend']) & (stock_data['Close'] > stock_data['R1'])
        sell_condition = (stock_data['Close'] < stock_data['SuperTrend'])
        
        stock_data['Buy_Signal'] = np.where(buy_condition, stock_data['Close'], np.nan)
        stock_data['Sell_Signal'] = np.where(sell_condition, stock_data['Close'], np.nan)
        
        return stock_data
    except Exception as e:
        # If trading strategy fails, return data with empty signals
        stock_data['Buy_Signal'] = np.nan
        stock_data['Sell_Signal'] = np.nan
        return stock_data

# Generate Trading Recommendation
def generate_recommendation(stock_data, ticker):
    """Generate comprehensive trading recommendation based on multiple indicators."""
    try:
        # Get latest values and handle NaN values properly
        # Handle multi-level columns by getting the actual scalar value
        current_price = stock_data['Close'].iloc[-1]
        if hasattr(current_price, 'item'):
            current_price = current_price.item()
        
        # Initialize scoring system with weights
        buy_signals = 0
        sell_signals = 0
        reasons = []
        total_possible_signals = 0
        
        # Helper function to safely get scalar values
        def get_scalar_value(column_name):
            if column_name in stock_data.columns:
                value = stock_data[column_name].iloc[-1]
                if hasattr(value, 'item'):
                    return value.item()
                return value
            return None
        
        # 1. Moving Average Analysis (Weight: 20%)
        current_sma_50 = get_scalar_value('SMA_50')
        if current_sma_50 is not None and not pd.isna(current_sma_50):
            total_possible_signals += 1
            if current_price > current_sma_50:
                buy_signals += 1
                reasons.append("✅ Price above 50-day SMA (bullish)")
            else:
                sell_signals += 1
                reasons.append("❌ Price below 50-day SMA (bearish)")
        
        current_sma_200 = get_scalar_value('SMA_200')
        if current_sma_200 is not None and not pd.isna(current_sma_200):
            total_possible_signals += 1.5
            if current_price > current_sma_200:
                buy_signals += 1.5  # Higher weight for 200-day
                reasons.append("✅ Price above 200-day SMA (strong bullish)")
            else:
                sell_signals += 1.5
                reasons.append("❌ Price below 200-day SMA (strong bearish)")
        
        # Check SMA crossover if both are available
        if (current_sma_50 is not None and current_sma_200 is not None and 
            not pd.isna(current_sma_50) and not pd.isna(current_sma_200)):
            total_possible_signals += 1
            if current_sma_50 > current_sma_200:
                buy_signals += 1
                reasons.append("✅ Golden Cross: 50-day SMA above 200-day SMA")
            else:
                sell_signals += 1
                reasons.append("❌ Death Cross: 50-day SMA below 200-day SMA")
        
        # 2. EMA Analysis (Weight: 15%)
        current_ema_50 = get_scalar_value('EMA_50')
        if current_ema_50 is not None and not pd.isna(current_ema_50):
            total_possible_signals += 0.8
            if current_price > current_ema_50:
                buy_signals += 0.8
                reasons.append("✅ Price above 50-day EMA (bullish)")
            else:
                sell_signals += 0.8
                reasons.append("❌ Price below 50-day EMA (bearish)")
        
        current_ema_200 = get_scalar_value('EMA_200')
        if current_ema_200 is not None and not pd.isna(current_ema_200):
            total_possible_signals += 1.2
            if current_price > current_ema_200:
                buy_signals += 1.2
                reasons.append("✅ Price above 200-day EMA (strong bullish)")
            else:
                sell_signals += 1.2
                reasons.append("❌ Price below 200-day EMA (strong bearish)")
        
        # 3. SuperTrend Analysis (Weight: 25% - Highest weight)
        current_supertrend = get_scalar_value('SuperTrend')
        if current_supertrend is not None and not pd.isna(current_supertrend):
            total_possible_signals += 2.5
            if current_price > current_supertrend:
                buy_signals += 2.5
                reasons.append("✅ Price above SuperTrend (strong buy signal)")
            else:
                sell_signals += 2.5
                reasons.append("❌ Price below SuperTrend (strong sell signal)")
        
        # 4. MACD Analysis (Weight: 20%)
        current_macd = get_scalar_value('MACD')
        current_signal = get_scalar_value('Signal_Line')
        if (current_macd is not None and current_signal is not None and 
            not pd.isna(current_macd) and not pd.isna(current_signal)):
            total_possible_signals += 1
            if current_macd > current_signal:
                buy_signals += 1
                reasons.append("✅ MACD above Signal Line (bullish momentum)")
            else:
                sell_signals += 1
                reasons.append("❌ MACD below Signal Line (bearish momentum)")
        
        if current_macd is not None and not pd.isna(current_macd):
            total_possible_signals += 1
            if current_macd > 0:
                buy_signals += 1
                reasons.append("✅ MACD above zero line (positive momentum)")
            else:
                sell_signals += 1
                reasons.append("❌ MACD below zero line (negative momentum)")
        
        # 5. Bollinger Bands Analysis (Weight: 10%)
        current_upper_bb = get_scalar_value('Upper_Band')
        current_lower_bb = get_scalar_value('Lower_Band')
        if (current_upper_bb is not None and current_lower_bb is not None and 
            not pd.isna(current_upper_bb) and not pd.isna(current_lower_bb)):
            total_possible_signals += 1
            if current_price < current_lower_bb:
                buy_signals += 1
                reasons.append("✅ Price near lower Bollinger Band (potential oversold)")
            elif current_price > current_upper_bb:
                sell_signals += 1
                reasons.append("❌ Price near upper Bollinger Band (potential overbought)")
            else:
                buy_signals += 0.5
                reasons.append("➡️ Price within Bollinger Bands (neutral)")
        
        # 6. Pivot Points Analysis (Weight: 10%)
        current_r1 = get_scalar_value('R1')
        current_s1 = get_scalar_value('S1')
        if (current_r1 is not None and current_s1 is not None and 
            not pd.isna(current_r1) and not pd.isna(current_s1)):
            total_possible_signals += 1
            if current_price > current_r1:
                buy_signals += 1
                reasons.append("✅ Price above R1 resistance (bullish breakout)")
            elif current_price < current_s1:
                sell_signals += 1
                reasons.append("❌ Price below S1 support (bearish breakdown)")
            else:
                buy_signals += 0.5
                reasons.append("➡️ Price between S1 and R1 (neutral)")
        
        # 7. Volume Analysis (Weight: 5%)
        current_volume = get_scalar_value('Volume')
        avg_volume = get_scalar_value('Volume_Trend')
        if (current_volume is not None and avg_volume is not None and 
            not pd.isna(current_volume) and not pd.isna(avg_volume) and avg_volume > 0):
            total_possible_signals += 0.5
            if current_volume > avg_volume * 1.5:
                buy_signals += 0.5
                reasons.append("✅ High volume (confirms price movement)")
            elif current_volume < avg_volume * 0.5:
                sell_signals += 0.5
                reasons.append("⚠️ Low volume (weakens price movement)")
        
        # Determine recommendation based on weighted signals
        if total_possible_signals > 0:
            buy_percentage = (buy_signals / total_possible_signals) * 100
        else:
            buy_percentage = 50
        
        if buy_percentage >= 75:
            recommendation = "🟢 STRONG BUY"
            confidence = "High"
            action = "Consider buying with stop loss"
        elif buy_percentage >= 65:
            recommendation = "🟡 BUY"
            confidence = "Medium"
            action = "Consider buying with caution"
        elif buy_percentage >= 45:
            recommendation = "🟠 HOLD"
            confidence = "Low"
            action = "Wait for clearer signals"
        elif buy_percentage >= 35:
            recommendation = "🔴 SELL"
            confidence = "Medium"
            action = "Consider selling with caution"
        else:
            recommendation = "🔴 STRONG SELL"
            confidence = "High"
            action = "Consider selling with stop loss"
        
        # Calculate risk metrics
        volatility = (stock_data['Close'].pct_change().std() * np.sqrt(252) * 100).item()
        max_drawdown = ((stock_data['Close'].max() - stock_data['Close'].min()) / stock_data['Close'].max() * 100).item()
        
        # Get support and resistance levels
        support_level = get_scalar_value('S1') or 0
        resistance_level = get_scalar_value('R1') or 0
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'action': action,
            'buy_percentage': buy_percentage,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'reasons': reasons,
            'current_price': current_price,
            'volatility': volatility,
            'max_drawdown': max_drawdown,
            'support_level': support_level,
            'resistance_level': resistance_level
        }
        
    except Exception as e:
        return {
            'recommendation': "⚠️ UNABLE TO ANALYZE",
            'confidence': "Unknown",
            'action': "Check data availability",
            'buy_percentage': 50,
            'buy_signals': 0,
            'sell_signals': 0,
            'reasons': [f"Error in analysis: {str(e)}"],
            'current_price': 0,
            'volatility': 0,
            'max_drawdown': 0,
            'support_level': 0,
            'resistance_level': 0
        }

# Plot Indicators using Plotly
def plot_indicators(stock_data, ticker):
    """Create interactive plots using Plotly."""
    figures = {}
    
    # Use original data but handle NaN values properly for each indicator
    plot_data = stock_data.copy()
    
    # 1. Moving Averages Plot
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=plot_data.index, y=plot_data['Close'], mode='lines', name=f'{ticker} Close Price', line=dict(color='#1f77b4', width=2)))
    
    # Only add moving averages if they exist and have data
    if 'SMA_50' in plot_data.columns:
        sma_50_data = plot_data['SMA_50'].dropna()
        if len(sma_50_data) > 0:
            fig_ma.add_trace(go.Scatter(x=sma_50_data.index, y=sma_50_data, mode='lines', name='50-Day SMA', line=dict(color='#ff7f0e', width=1.5)))
    
    if 'SMA_200' in plot_data.columns:
        sma_200_data = plot_data['SMA_200'].dropna()
        if len(sma_200_data) > 0:
            fig_ma.add_trace(go.Scatter(x=sma_200_data.index, y=sma_200_data, mode='lines', name='200-Day SMA', line=dict(color='#2ca02c', width=1.5)))
    
    if 'EMA_50' in plot_data.columns:
        ema_50_data = plot_data['EMA_50'].dropna()
        if len(ema_50_data) > 0:
            fig_ma.add_trace(go.Scatter(x=ema_50_data.index, y=ema_50_data, mode='lines', name='50-Day EMA', line=dict(color='#d62728', width=1.5)))
    
    if 'EMA_200' in plot_data.columns:
        ema_200_data = plot_data['EMA_200'].dropna()
        if len(ema_200_data) > 0:
            fig_ma.add_trace(go.Scatter(x=ema_200_data.index, y=ema_200_data, mode='lines', name='200-Day EMA', line=dict(color='#9467bd', width=1.5)))
    
    fig_ma.update_layout(title=f'{ticker} Stock Price with Moving Averages', xaxis_title='Date', yaxis_title='Close Price', template='plotly_white', height=400)
    figures['Moving_Averages'] = fig_ma
    
    # 2. Bollinger Bands Plot
    fig_bb = go.Figure()
    fig_bb.add_trace(go.Scatter(x=plot_data.index, y=plot_data['Close'], mode='lines', name=f'{ticker} Close Price', line=dict(color='#1f77b4', width=2)))
    
    if 'Upper_Band' in plot_data.columns:
        upper_band_data = plot_data['Upper_Band'].dropna()
        if len(upper_band_data) > 0:
            fig_bb.add_trace(go.Scatter(x=upper_band_data.index, y=upper_band_data, mode='lines', name='Upper Bollinger Band', line=dict(color='#d62728', width=1.5)))
    
    if 'Lower_Band' in plot_data.columns:
        lower_band_data = plot_data['Lower_Band'].dropna()
        if len(lower_band_data) > 0:
            fig_bb.add_trace(go.Scatter(x=lower_band_data.index, y=lower_band_data, mode='lines', name='Lower Bollinger Band', line=dict(color='#d62728', width=1.5), fill='tonexty'))
    
    fig_bb.update_layout(title=f'{ticker} Stock Price with Bollinger Bands', xaxis_title='Date', yaxis_title='Close Price', template='plotly_white', height=400)
    figures['Bollinger_Bands'] = fig_bb
    
    # 3. MACD Plot
    fig_macd = go.Figure()
    if 'MACD' in plot_data.columns:
        macd_data = plot_data['MACD'].dropna()
        if len(macd_data) > 0:
            fig_macd.add_trace(go.Scatter(x=macd_data.index, y=macd_data, mode='lines', name='MACD', line=dict(color='#1f77b4', width=2)))
    
    if 'Signal_Line' in plot_data.columns:
        signal_data = plot_data['Signal_Line'].dropna()
        if len(signal_data) > 0:
            fig_macd.add_trace(go.Scatter(x=signal_data.index, y=signal_data, mode='lines', name='Signal Line', line=dict(color='#ff7f0e', width=2)))
    
    fig_macd.add_hline(y=0, line_dash="dash", line_color="red")
    fig_macd.update_layout(title=f'{ticker} MACD and Signal Line', xaxis_title='Date', yaxis_title='Value', template='plotly_white', height=400)
    figures['MACD'] = fig_macd
    
    # 4. Volume Trend Plot
    fig_volume = go.Figure()
    if 'Volume_Trend' in plot_data.columns:
        volume_data = plot_data['Volume_Trend'].dropna()
        if len(volume_data) > 0:
            fig_volume.add_trace(go.Scatter(x=volume_data.index, y=volume_data, mode='lines', name='20-Day Volume Trend', line=dict(color='#2ca02c', width=2)))
    
    fig_volume.update_layout(title=f'{ticker} Volume Trend', xaxis_title='Date', yaxis_title='Volume', template='plotly_white', height=400)
    figures['Volume_Trend'] = fig_volume
    
    # 5. SuperTrend Plot
    fig_supertrend = go.Figure()
    fig_supertrend.add_trace(go.Scatter(x=plot_data.index, y=plot_data['Close'], mode='lines', name=f'{ticker} Close Price', line=dict(color='#1f77b4', width=2)))
    
    if 'SuperTrend' in plot_data.columns:
        supertrend_data = plot_data['SuperTrend'].dropna()
        if len(supertrend_data) > 0:
            fig_supertrend.add_trace(go.Scatter(x=supertrend_data.index, y=supertrend_data, mode='lines', name='SuperTrend', line=dict(color='#9467bd', width=2)))
    
    fig_supertrend.update_layout(title=f'{ticker} SuperTrend', xaxis_title='Date', yaxis_title='Close Price', template='plotly_white', height=400)
    figures['SuperTrend'] = fig_supertrend
    
    # 6. Trading Signals Plot
    fig_signals = go.Figure()
    fig_signals.add_trace(go.Scatter(x=plot_data.index, y=plot_data['Close'], mode='lines', name=f'{ticker} Close Price', line=dict(color='#1f77b4', width=2)))
    
    if 'Buy_Signal' in plot_data.columns:
        buy_signals = plot_data[plot_data['Buy_Signal'].notna()]
        if len(buy_signals) > 0:
            fig_signals.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Buy_Signal'], mode='markers', name='Buy Signal', marker=dict(color='green', size=8, symbol='triangle-up')))
    
    if 'Sell_Signal' in plot_data.columns:
        sell_signals = plot_data[plot_data['Sell_Signal'].notna()]
        if len(sell_signals) > 0:
            fig_signals.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Sell_Signal'], mode='markers', name='Sell Signal', marker=dict(color='red', size=8, symbol='triangle-down')))
    
    fig_signals.update_layout(title=f'{ticker} Trading Signals', xaxis_title='Date', yaxis_title='Close Price', template='plotly_white', height=400)
    figures['Trading_Signals'] = fig_signals
    
    return figures

def main():
    """Main function to run the Streamlit app."""
    
    # Check authentication first
    if not main_auth():
        return  # Stop execution if user is not authenticated
    
    # Initialize session state
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = "AAPL"
    if 'favorites' not in st.session_state:
        st.session_state.favorites = ["AAPL", "MSFT", "GOOGL"]
    
    # Header
    st.markdown('<h1 class="main-header">📈 Trading Strategy Simulator</h1>', unsafe_allow_html=True)
    
    # Welcome message for authenticated user
    st.success(f"Welcome back, {st.session_state.username}! 🎉")
    
    # Platform statistics
    st.subheader("📊 Platform Statistics")
    stats = auth_manager.get_user_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", stats['total_users'], help="All registered users since launch")
    with col2:
        st.metric("Total Analyses", stats['total_analyses'], help="All analyses performed")
    with col3:
        st.metric("Active Users", stats['active_users'], help="Users active in last 30 days")
    
    # Most popular stocks section
    st.markdown("---")
    st.subheader("🔥 Most Popular Stocks")
    
    popular_stocks = auth_manager.get_popular_stocks(limit=10)
    
    if popular_stocks:
        # Create columns for the popular stocks display
        cols = st.columns(5)
        
        for i, stock in enumerate(popular_stocks[:10]):
            col_idx = i % 5
            with cols[col_idx]:
                # Create a clickable button for each popular stock
                if st.button(
                    f"📈 {stock['ticker']}\n🔍 {stock['count']} searches", 
                    key=f"popular_{stock['ticker']}",
                    help=f"Last searched: {stock['last_searched'][:10] if stock['last_searched'] != 'N/A' else 'Never'}"
                ):
                    st.session_state.selected_ticker = stock['ticker']
                    st.rerun()
        
        # Show detailed table in an expander
        with st.expander("📋 Detailed Popular Stocks List"):
            if popular_stocks:
                # Create a DataFrame for better display
                import pandas as pd
                df = pd.DataFrame(popular_stocks)
                df['Rank'] = range(1, len(df) + 1)
                df = df[['Rank', 'ticker', 'count', 'last_searched']]
                df.columns = ['Rank', 'Stock', 'Searches', 'Last Searched']
                
                # Format the last searched date
                df['Last Searched'] = df['Last Searched'].apply(
                    lambda x: x[:10] if x != 'N/A' else 'Never'
                )
                
                st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No stock searches recorded yet. Start analyzing stocks to see popular trends!")
    
    # Sidebar
    st.sidebar.header("📊 Analysis Settings")
    
    # Stock ticker input
    ticker = st.sidebar.text_input(
        "Stock Ticker",
        value=st.session_state.selected_ticker,
        placeholder="e.g., AAPL, MSFT, TSLA, ITC.NS"
    ).upper()
    
    # Update session state when ticker is manually changed
    if ticker != st.session_state.selected_ticker:
        st.session_state.selected_ticker = ticker
    
    # Date range selection
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Favorites Management
    st.sidebar.header("⭐ Favorites")
    
    # Add new favorite
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        new_favorite = st.text_input(
            "Add Favorite",
            placeholder="e.g., TSLA",
            key="new_favorite_input"
        ).upper()
    
    with col2:
        if st.button("➕", help="Add to favorites"):
            if new_favorite and new_favorite not in st.session_state.favorites:
                st.session_state.favorites.append(new_favorite)
                st.rerun()
    
    # Display favorites with remove buttons
    if st.session_state.favorites:
        st.sidebar.write("**Your Favorites:**")
        for i, fav in enumerate(st.session_state.favorites):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if st.button(fav, key=f"fav_btn_{fav}"):
                    st.session_state.selected_ticker = fav
                    st.rerun()
            with col2:
                if st.button("📊", key=f"analyze_{fav}", help=f"Analyze {fav}"):
                    st.session_state.selected_ticker = fav
                    st.rerun()
            with col3:
                if st.button("❌", key=f"remove_{fav}", help=f"Remove {fav} from favorites"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()
        
        # Clear all favorites option
        if st.sidebar.button("🗑️ Clear All Favorites", help="Remove all favorites"):
            st.session_state.favorites = []
            st.rerun()
    else:
        st.sidebar.info("No favorites added yet. Add some stocks to get started!")
    
    # Quick actions
    st.sidebar.header("⚡ Quick Actions")
    
    # Show most popular stocks from user searches
    st.sidebar.subheader("🔥 Most Searched")
    popular_searches = auth_manager.get_popular_stocks(limit=5)
    
    if popular_searches:
        for stock in popular_searches:
            if st.sidebar.button(f"📈 {stock['ticker']} ({stock['count']})", key=f"sidebar_popular_{stock['ticker']}"):
                st.session_state.selected_ticker = stock['ticker']
                st.rerun()
    else:
        st.sidebar.info("No searches yet")
    
    st.sidebar.subheader("📊 Popular Stocks")
    popular_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "ITC.NS", "RELIANCE.NS"]
    
    # Create columns for better button layout
    col1, col2 = st.sidebar.columns(2)
    for i, stock in enumerate(popular_stocks):
        if i % 2 == 0:
            if col1.button(stock, key=f"btn_{stock}"):
                st.session_state.selected_ticker = stock
                st.rerun()
        else:
            if col2.button(stock, key=f"btn_{stock}"):
                st.session_state.selected_ticker = stock
                st.rerun()
    
    # Use the session state ticker for analysis
    ticker = st.session_state.selected_ticker
    
    # Add current ticker to favorites option
    if ticker and ticker not in st.session_state.favorites:
        if st.sidebar.button("⭐ Add to Favorites", help=f"Add {ticker} to your favorites"):
            st.session_state.favorites.append(ticker)
            st.rerun()
    
    if ticker and start_date and end_date:
        if start_date >= end_date:
            st.error("Start date must be before end date.")
            return
        
        # Fetch data
        with st.spinner(f"Fetching data for {ticker}..."):
            stock_data = fetch_data(ticker, start_date, end_date)
        
        if stock_data is not None and not stock_data.empty:
            # Increment user's analysis count and track stock search
            auth_manager.increment_analysis_count(st.session_state.username)
            auth_manager.track_stock_search(ticker)
            
            # Preprocess and calculate indicators
            with st.spinner("Calculating technical indicators..."):
                stock_data = preprocess_data(stock_data)
                stock_data = calculate_moving_averages(stock_data)
                stock_data = calculate_macd(stock_data)
                stock_data = calculate_bollinger_bands(stock_data)
                stock_data = volume_trend(stock_data)
                stock_data = calculate_supertrend(stock_data)
                stock_data = calculate_pivot_points(stock_data)
                stock_data = trading_strategy(stock_data)
            
            # Display current price and basic info
            current_price = stock_data['Close'].iloc[-1].item()
            price_change = ((current_price - stock_data['Close'].iloc[0].item()) / stock_data['Close'].iloc[0].item()) * 100
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"${current_price:.2f}")
            with col2:
                st.metric("Total Return", f"{price_change:.2f}%")
            with col3:
                volume = stock_data['Volume'].iloc[-1].item()
                st.metric("Volume", f"{volume:,}")
            with col4:
                volatility = (stock_data['Close'].pct_change().std() * np.sqrt(252) * 100).item()
                st.metric("Volatility", f"{volatility:.2f}%")
            
            # Charts
            st.header("📈 Technical Analysis Charts")
            
            # Generate all plots
            figures = plot_indicators(stock_data, ticker)
            
            # Display charts in tabs
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Moving Averages", "Bollinger Bands", "MACD", 
                "Volume Trend", "SuperTrend", "Trading Signals"
            ])
            
            with tab1:
                st.plotly_chart(figures['Moving_Averages'], use_container_width=True, key="moving_averages_chart")
                st.write("**Moving Averages Analysis**: Shows 50-day and 200-day SMA and EMA. Price above moving averages indicates bullish trend.")
            
            with tab2:
                st.plotly_chart(figures['Bollinger_Bands'], use_container_width=True, key="bollinger_bands_chart")
                st.write("**Bollinger Bands Analysis**: Shows price volatility. Price touching bands suggests potential reversal.")
            
            with tab3:
                st.plotly_chart(figures['MACD'], use_container_width=True, key="macd_chart")
                st.write("**MACD Analysis**: Shows MACD line and signal line. MACD above signal line indicates bullish momentum.")
            
            with tab4:
                st.plotly_chart(figures['Volume_Trend'], use_container_width=True, key="volume_trend_chart")
                st.write("**Volume Trend Analysis**: Shows 20-day volume trend. Higher volume confirms price movements.")
            
            with tab5:
                st.plotly_chart(figures['SuperTrend'], use_container_width=True, key="supertrend_chart")
                st.write("**SuperTrend Analysis**: Shows SuperTrend indicator. Price above SuperTrend indicates bullish trend.")
            
            with tab6:
                st.plotly_chart(figures['Trading_Signals'], use_container_width=True, key="trading_signals_chart")
                st.write("**Trading Signals**: Green triangles show buy signals, red triangles show sell signals based on SuperTrend and pivot points.")
            
            # Summary statistics
            st.header("📊 Summary Statistics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Price Statistics")
                high_price = stock_data['High'].max().item()
                low_price = stock_data['Low'].min().item()
                price_range = high_price - low_price
                st.write(f"**Period High**: ${high_price:.2f}")
                st.write(f"**Period Low**: ${low_price:.2f}")
                st.write(f"**Price Range**: ${price_range:.2f}")
            
            with col2:
                st.subheader("Moving Average Analysis")
                sma_50 = stock_data['SMA_50'].iloc[-1].item()
                sma_200 = stock_data['SMA_200'].iloc[-1].item()
                st.write(f"**50-Day SMA**: ${sma_50:.2f}")
                st.write(f"**200-Day SMA**: ${sma_200:.2f}")
                st.write(f"**SMA Ratio**: {sma_50/sma_200:.3f}")
            
            with col3:
                st.subheader("Technical Indicators")
                macd_current = stock_data['MACD'].iloc[-1].item()
                macd_signal = stock_data['Signal_Line'].iloc[-1].item()
                supertrend_current = stock_data['SuperTrend'].iloc[-1].item()
                st.write(f"**MACD**: {macd_current:.4f}")
                st.write(f"**MACD Signal**: {macd_signal:.4f}")
                st.write(f"**SuperTrend**: ${supertrend_current:.2f}")
            
            # Trading Recommendation Section
            st.header("🎯 Trading Recommendation")
            
            # Generate recommendation
            recommendation_data = generate_recommendation(stock_data, ticker)
            
            # Main recommendation display
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;'>
                    <h3 style='margin: 0; color: #1f77b4;'>{recommendation_data['recommendation']}</h3>
                    <p style='margin: 5px 0; font-size: 16px;'><strong>Action:</strong> {recommendation_data['action']}</p>
                    <p style='margin: 5px 0; font-size: 14px;'><strong>Confidence:</strong> {recommendation_data['confidence']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Buy Signals", f"{recommendation_data['buy_signals']:.1f}")
            
            with col3:
                st.metric("Sell Signals", f"{recommendation_data['sell_signals']:.1f}")
            
            # Signal strength indicator
            st.subheader("📊 Signal Strength")
            buy_percentage = recommendation_data['buy_percentage']
            
            # Create a visual progress bar
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.progress(buy_percentage / 100)
                st.write(f"**Buy Signal Strength: {buy_percentage:.1f}%**")
            
            # Risk metrics
            st.subheader("⚠️ Risk Analysis")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Volatility", f"{recommendation_data['volatility']:.2f}%")
            
            with col2:
                st.metric("Max Drawdown", f"{recommendation_data['max_drawdown']:.2f}%")
            
            with col3:
                st.metric("Support Level", f"${recommendation_data['support_level']:.2f}")
            
            with col4:
                st.metric("Resistance Level", f"${recommendation_data['resistance_level']:.2f}")
            
            # Detailed analysis
            st.subheader("🔍 Detailed Analysis")
            
            # Display reasons in a nice format
            reasons = recommendation_data['reasons']
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Technical Indicators Analysis:**")
                for i, reason in enumerate(reasons[:len(reasons)//2]):
                    st.write(f"• {reason}")
            
            with col2:
                st.write("**Additional Factors:**")
                for i, reason in enumerate(reasons[len(reasons)//2:]):
                    st.write(f"• {reason}")
            
            # Trading advice
            st.subheader("💡 Trading Advice")
            
            if "STRONG BUY" in recommendation_data['recommendation']:
                st.success("""
                **Strong Buy Recommendation:**
                - Consider entering a long position
                - Set stop loss at support level
                - Monitor for any reversal signals
                - Consider position sizing based on risk tolerance
                """)
            elif "BUY" in recommendation_data['recommendation']:
                st.info("""
                **Buy Recommendation:**
                - Consider a small long position
                - Set tight stop loss
                - Wait for confirmation signals
                - Monitor market conditions closely
                """)
            elif "HOLD" in recommendation_data['recommendation']:
                st.warning("""
                **Hold Recommendation:**
                - Wait for clearer market direction
                - Monitor key support/resistance levels
                - Consider reducing position size
                - Stay alert for breakout signals
                """)
            elif "SELL" in recommendation_data['recommendation']:
                st.error("""
                **Sell Recommendation:**
                - Consider reducing long positions
                - Set stop loss at resistance level
                - Monitor for reversal signals
                - Consider hedging strategies
                """)
            elif "STRONG SELL" in recommendation_data['recommendation']:
                st.error("""
                **Strong Sell Recommendation:**
                - Consider exiting long positions
                - Set tight stop loss
                - Monitor for any bullish reversal
                - Consider short positions with caution
                """)
            
            # Disclaimer
            st.markdown("""
            ---
            **⚠️ Important Disclaimer:**
            - This analysis is for educational purposes only
            - Not financial advice - always do your own research
            - Past performance doesn't guarantee future results
            - Consider consulting with a financial advisor
            - Always use proper risk management strategies
            """)
        
        else:
            st.error(f"Could not fetch data for {ticker}. Please check the ticker symbol and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>📈 Trading Strategy Simulator | Built with Streamlit | Data from Yahoo Finance</p>
            <p>⚠️ This tool is for educational purposes only. Not financial advice.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 