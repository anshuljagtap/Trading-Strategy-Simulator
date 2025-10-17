# 🚀 Deploy to Streamlit Cloud

## Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already)
2. **Push your code** to GitHub
3. **Make sure these files are in your repo:**
   - `trading_simulator.py`
   - `auth.py`
   - `requirements.txt`
   - `data_persistence.py`
   - `keep_alive.py`
   - `.streamlit/config.toml`

## Step 2: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the details:**
   - **Repository**: `your-username/your-repo-name`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `trading_simulator.py`
   - **App URL**: Choose a custom URL (optional)

## Step 3: Configure for Production

### Update requirements.txt for Streamlit Cloud:
```
streamlit>=1.28.0
yfinance>=0.2.18
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
requests>=2.31.0
watchdog>=3.0.0
```

### Create .streamlit/secrets.toml for production:
```toml
[general]
# Add any secrets here if needed
```

## Step 4: Handle Data Persistence

**Important**: Streamlit Cloud has limitations with file persistence. You'll need to:

1. **Use Streamlit's built-in session state** for temporary data
2. **Consider using a database** for permanent storage:
   - **SQLite** (file-based, works on Streamlit Cloud)
   - **PostgreSQL** (external service like Supabase)
   - **MongoDB Atlas** (cloud database)

## Step 5: Update Your App for Cloud

### Modify data_persistence.py for cloud compatibility:
```python
import os
import streamlit as st

def get_data_dir():
    """Get data directory, create if it doesn't exist."""
    if 'STREAMLIT_SHARING' in os.environ:
        # Running on Streamlit Cloud
        data_dir = "/tmp/data"
    else:
        # Running locally
        data_dir = "data"
    
    os.makedirs(data_dir, exist_ok=True)
    return data_dir
```

## Step 6: Deploy!

1. **Click "Deploy!"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Your app will be live** at: `https://your-app-name.streamlit.app`

## 🎉 Benefits of Streamlit Cloud:

- ✅ **Free hosting**
- ✅ **Automatic HTTPS**
- ✅ **Custom domains** (with paid plan)
- ✅ **Easy updates** (just push to GitHub)
- ✅ **Built for Streamlit**
- ✅ **No server management**

## ⚠️ Limitations:

- ❌ **Apps sleep** after 1 hour of inactivity
- ❌ **Limited file persistence** (files reset on restart)
- ❌ **No background processes** (keep-alive won't work)
- ❌ **Resource limits** on free tier

## 🔧 Alternative: Railway Deployment

If you want more control and no sleeping issues:

1. **Go to**: https://railway.app/
2. **Connect GitHub**
3. **Deploy from repository**
4. **Set environment variables**
5. **Deploy!**

Railway gives you:
- ✅ **No sleeping**
- ✅ **Persistent storage**
- ✅ **Background processes**
- ✅ **Custom domains**
- ❌ **Paid service** (but very affordable)

## 📊 Recommendation:

**Start with Streamlit Cloud** - it's free and perfect for showcasing your app. If you need more features later, you can always migrate to Railway or another service.
