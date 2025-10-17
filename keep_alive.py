#!/usr/bin/env python3
"""
Keep Alive Script for Streamlit Trading Simulator
This script prevents the Streamlit app from sleeping by sending periodic requests.
"""

import requests
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)

class StreamlitKeepAlive:
    def __init__(self, url="http://localhost:8501", interval=300):
        """
        Initialize the keep-alive service.
        
        Args:
            url (str): URL of the Streamlit app
            interval (int): Interval between requests in seconds (default: 5 minutes)
        """
        self.url = url
        self.interval = interval
        self.running = False
        
    def ping_app(self):
        """Send a ping request to keep the app alive."""
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                logging.info(f"✅ App is alive - Status: {response.status_code}")
                return True
            else:
                logging.warning(f"⚠️ App responded with status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Failed to ping app: {e}")
            return False
    
    def start(self):
        """Start the keep-alive service."""
        self.running = True
        logging.info(f"🚀 Starting keep-alive service for {self.url}")
        logging.info(f"⏰ Ping interval: {self.interval} seconds")
        
        consecutive_failures = 0
        max_failures = 3
        
        while self.running:
            try:
                success = self.ping_app()
                
                if success:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        logging.error(f"💥 App failed {max_failures} consecutive times. Stopping keep-alive.")
                        break
                
                # Wait for the next ping
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                logging.info("🛑 Keep-alive service stopped by user")
                break
            except Exception as e:
                logging.error(f"💥 Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
        
        self.running = False
        logging.info("🏁 Keep-alive service stopped")
    
    def stop(self):
        """Stop the keep-alive service."""
        self.running = False

def main():
    """Main function to run the keep-alive service."""
    print("🔄 Streamlit Keep-Alive Service")
    print("=" * 40)
    
    # Get configuration from environment variables or use defaults
    url = os.getenv('STREAMLIT_URL', 'http://localhost:8501')
    interval = int(os.getenv('KEEP_ALIVE_INTERVAL', '300'))  # 5 minutes default
    
    print(f"🌐 Target URL: {url}")
    print(f"⏰ Ping interval: {interval} seconds")
    print(f"📝 Logs will be saved to: keep_alive.log")
    print("\nPress Ctrl+C to stop the service")
    print("=" * 40)
    
    # Create and start the keep-alive service
    keep_alive = StreamlitKeepAlive(url=url, interval=interval)
    
    try:
        keep_alive.start()
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"\n💥 Service crashed: {e}")

if __name__ == "__main__":
    main()
