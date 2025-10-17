#!/usr/bin/env python3
"""
Add sample stock searches to demonstrate the popular stocks feature
"""

from auth import auth_manager
import random

def add_sample_searches():
    """Add sample stock searches to demonstrate the feature."""
    
    # Popular stocks to add as samples
    sample_stocks = [
        "AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", 
        "NVDA", "META", "NFLX", "AMD", "INTC",
        "ITC.NS", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFC.NS"
    ]
    
    print("Adding sample stock searches...")
    
    # Add multiple searches for each stock to create realistic data
    for stock in sample_stocks:
        # Random number of searches between 1-15
        search_count = random.randint(1, 15)
        
        for _ in range(search_count):
            auth_manager.track_stock_search(stock)
        
        print(f"Added {search_count} searches for {stock}")
    
    print("\n✅ Sample searches added successfully!")
    print("Now you can see the most popular stocks feature in action.")
    
    # Show the current popular stocks
    popular = auth_manager.get_popular_stocks(limit=10)
    print(f"\n🔥 Top 10 Most Popular Stocks:")
    for i, stock in enumerate(popular, 1):
        print(f"{i:2d}. {stock['ticker']:10s} - {stock['count']:2d} searches")

if __name__ == "__main__":
    add_sample_searches()
