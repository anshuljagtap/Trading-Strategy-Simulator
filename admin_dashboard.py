import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard - Trading Strategy Simulator",
    page_icon="📊",
    layout="wide"
)

def load_users():
    """Load users from JSON file."""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def get_user_stats():
    """Get overall user statistics."""
    users = load_users()
    if not users:
        return {
            'total_users': 0,
            'total_analyses': 0,
            'active_users': 0,
            'popular_stocks': [],
            'user_growth': [],
            'daily_analyses': []
        }
    
    total_analyses = sum(len(user.get('analyses_performed', [])) for user in users.values())
    active_users = len([user for user in users.values() 
                       if (datetime.now() - datetime.fromisoformat(user['last_login'])).days < 30])
    
    # Get popular stocks
    all_stocks = []
    for user in users.values():
        all_stocks.extend(user.get('favorite_stocks', []))
    
    popular_stocks = Counter(all_stocks).most_common(10)
    
    # User growth over time
    user_growth = []
    for user in users.values():
        created_date = datetime.fromisoformat(user['created_date']).date()
        user_growth.append(created_date)
    
    user_growth_df = pd.DataFrame(user_growth, columns=['date'])
    user_growth_df = user_growth_df.groupby('date').size().reset_index(name='new_users')
    user_growth_df['cumulative_users'] = user_growth_df['new_users'].cumsum()
    
    # Daily analyses
    daily_analyses = []
    for user in users.values():
        for analysis in user.get('analyses_performed', []):
            analysis_date = datetime.fromisoformat(analysis['timestamp']).date()
            daily_analyses.append(analysis_date)
    
    daily_analyses_df = pd.DataFrame(daily_analyses, columns=['date'])
    daily_analyses_df = daily_analyses_df.groupby('date').size().reset_index(name='analyses')
    
    return {
        'total_users': len(users),
        'total_analyses': total_analyses,
        'active_users': active_users,
        'popular_stocks': popular_stocks,
        'user_growth': user_growth_df,
        'daily_analyses': daily_analyses_df
    }

def main():
    st.title("📊 Admin Dashboard - Trading Strategy Simulator")
    st.markdown("---")
    
    # Authentication (simple password check)
    admin_password = st.sidebar.text_input("Admin Password", type="password")
    if admin_password != "admin123":  # Change this to a secure password
        st.error("Please enter the correct admin password")
        return
    
    # Load statistics
    stats = get_user_stats()
    
    # Overview metrics
    st.header("📈 Platform Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", stats['total_users'], help="All registered users since launch")
    with col2:
        st.metric("Total Analyses", stats['total_analyses'], help="Total stock analyses performed")
    with col3:
        if stats['total_users'] > 0:
            avg_analyses = stats['total_analyses'] / stats['total_users']
            st.metric("Avg Analyses per User", f"{avg_analyses:.1f}", help="Average analyses per registered user")
        else:
            st.metric("Avg Analyses per User", "0")
    with col4:
        st.metric("Active Users (30 days)", stats['active_users'], help="Users who logged in within last 30 days")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 User Growth")
        if not stats['user_growth'].empty:
            fig = px.line(stats['user_growth'], x='date', y='cumulative_users', 
                         title="Cumulative User Growth")
            fig.update_layout(xaxis_title="Date", yaxis_title="Total Users")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No user growth data available")
    
    with col2:
        st.subheader("📊 Daily Analyses")
        if not stats['daily_analyses'].empty:
            fig = px.bar(stats['daily_analyses'], x='date', y='analyses', 
                        title="Daily Analysis Activity")
            fig.update_layout(xaxis_title="Date", yaxis_title="Number of Analyses")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No analysis data available")
    
    # Popular stocks
    st.subheader("⭐ Most Popular Stocks")
    if stats['popular_stocks']:
        stocks_df = pd.DataFrame(stats['popular_stocks'], columns=['Stock', 'Count'])
        fig = px.bar(stocks_df, x='Stock', y='Count', 
                    title="Most Popular Stocks Among Users")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No favorite stocks data available")
    
    # User details table
    st.subheader("👤 User Details")
    users = load_users()
    if users:
        user_data = []
        for email, user in users.items():
            user_data.append({
                'Email': email,
                'Name': user.get('name', 'N/A'),
                'Created': user.get('created_date', 'N/A')[:10],
                'Last Login': user.get('last_login', 'N/A')[:10],
                'Analyses': len(user.get('analyses_performed', [])),
                'Login Count': user.get('usage_count', 0),
                'Favorite Stocks': len(user.get('favorite_stocks', []))
            })
        
        df = pd.DataFrame(user_data)
        st.dataframe(df, use_container_width=True)
        
        # Export data
        if st.button("📥 Export User Data"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="user_data.csv",
                mime="text/csv"
            )
    else:
        st.info("No users registered yet")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    all_activities = []
    for email, user in users.items():
        for activity in user.get('analyses_performed', [])[-5:]:  # Last 5 activities per user
            all_activities.append({
                'User': user.get('name', email),
                'Action': activity['action'],
                'Timestamp': activity['timestamp'][:19],
                'Details': activity.get('details', '')
            })
    
    if all_activities:
        # Sort by timestamp
        all_activities.sort(key=lambda x: x['Timestamp'], reverse=True)
        activity_df = pd.DataFrame(all_activities[:20])  # Show last 20 activities
        st.dataframe(activity_df, use_container_width=True)
    else:
        st.info("No recent activity")
    
    # Platform insights
    st.subheader("💡 Platform Insights")
    if stats['total_users'] > 0:
        # Add a prominent total users display
        st.markdown(f"""
        <div style='background-color: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: #1f77b4;'>🎉 Total Users: {stats['total_users']}</h3>
            <p style='margin: 5px 0; font-size: 16px;'>Your platform has <strong>{stats['total_users']}</strong> registered users!</p>
            <p style='margin: 5px 0; font-size: 14px;'>Total analyses performed: <strong>{stats['total_analyses']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **User Engagement:**
            - Average analyses per user: {stats['total_analyses'] / stats['total_users']:.1f}
            - Active user rate: {(stats['active_users'] / stats['total_users']) * 100:.1f}%
            - Most active period: {stats['daily_analyses']['date'].mode().iloc[0] if not stats['daily_analyses'].empty else 'N/A'}
            """)
        
        with col2:
            st.success(f"""
            **Growth Metrics:**
            - Total users: {stats['total_users']}
            - Total analyses: {stats['total_analyses']}
            - Platform usage: {stats['total_analyses'] / max(stats['total_users'], 1):.1f} analyses/user
            - Popular stock: {stats['popular_stocks'][0][0] if stats['popular_stocks'] else 'N/A'}
            """)
    else:
        st.info("No users registered yet. Start promoting your platform!")

if __name__ == "__main__":
    main() 