# 🚀 Deployment Guide for Trading Strategy Simulator

This guide will help you deploy your trading simulator so others can access it online.

## 📋 Prerequisites

- GitHub account (free)
- All project files are ready
- `requirements.txt` is updated

## 🎯 Option 1: Streamlit Cloud (Recommended - FREE)

### Step 1: Push to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Trading Strategy Simulator"

# Create a new repository on GitHub.com
# Then push your code
git remote add origin https://github.com/YOUR_USERNAME/trading-strategy-simulator.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `trading-strategy-simulator`
5. Set the main file path: `trading_simulator.py`
6. Click "Deploy!"

**Your app will be live at:** `https://your-app-name.streamlit.app`

## 🌐 Option 2: Heroku (Paid)

### Step 1: Create Heroku Files
Create `Procfile`:
```
web: streamlit run trading_simulator.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Step 2: Deploy
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-trading-app
git push heroku main
```

## ☁️ Option 3: Google Cloud Platform

### Step 1: Create app.yaml
```yaml
runtime: python39
entrypoint: streamlit run trading_simulator.py --server.port=8080 --server.address=0.0.0.0

env_variables:
  STREAMLIT_SERVER_PORT: 8080
  STREAMLIT_SERVER_ADDRESS: 0.0.0.0
```

### Step 2: Deploy
```bash
gcloud app deploy
```

## 🐳 Option 4: Docker

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "trading_simulator.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build and Run
```bash
docker build -t trading-simulator .
docker run -p 8501:8501 trading-simulator
```

## 📱 Option 5: Local Network Sharing

### For sharing on your local network:
```bash
# Run with network access
streamlit run trading_simulator.py --server.address=0.0.0.0 --server.port=8501
```

Others on your network can access: `http://YOUR_IP:8501`

## 🔧 Configuration Tips

### Environment Variables
You can set these in your deployment platform:
- `STREAMLIT_SERVER_PORT`: Port number
- `STREAMLIT_SERVER_ADDRESS`: Server address
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: false

### Performance Optimization
- Use caching for expensive operations
- Limit data fetch periods
- Optimize chart rendering

## 🚨 Important Notes

1. **Data Source**: The app uses Yahoo Finance API (free tier)
2. **Rate Limits**: Be aware of API rate limits
3. **Security**: Add authentication if needed
4. **Costs**: Most options are free for basic usage

## 🎉 Success!

Once deployed, you can share the URL with anyone and they can use your trading simulator!

## 📞 Support

If you encounter issues:
1. Check the deployment platform logs
2. Verify all dependencies are in `requirements.txt`
3. Ensure the main file path is correct
4. Test locally before deploying

---

**Recommended for beginners:** Streamlit Cloud (Option 1)
**Best for production:** Heroku or Google Cloud
**Best for customization:** Docker 