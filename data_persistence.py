#!/usr/bin/env python3
"""
Data Persistence Module for Streamlit Trading Simulator
This module handles saving and loading user data, stats, and analysis history.
"""

import json
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPersistence:
    def __init__(self, data_dir="data"):
        """
        Initialize the data persistence system.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.ensure_data_directory()
        
        # File paths
        self.users_file = os.path.join(data_dir, "users.json")
        self.stats_file = os.path.join(data_dir, "stats.json")
        self.analysis_history_file = os.path.join(data_dir, "analysis_history.json")
        self.session_data_file = os.path.join(data_dir, "session_data.pkl")
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
    
    def save_users(self, users: Dict[str, Any]):
        """Save user data to JSON file."""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2, default=str)
            logger.info(f"Saved {len(users)} users to {self.users_file}")
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
    
    def load_users(self) -> Dict[str, Any]:
        """Load user data from JSON file."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                logger.info(f"Loaded {len(users)} users from {self.users_file}")
                return users
            else:
                logger.info("No users file found, returning empty dict")
                return {}
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            return {}
    
    def save_stats(self, stats: Dict[str, Any]):
        """Save application statistics."""
        try:
            # Add timestamp
            stats['last_updated'] = datetime.now().isoformat()
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            logger.info(f"Saved stats to {self.stats_file}")
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")
    
    def load_stats(self) -> Dict[str, Any]:
        """Load application statistics."""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
                logger.info(f"Loaded stats from {self.stats_file}")
                return stats
            else:
                # Return default stats
                default_stats = {
                    'total_users': 0,
                    'total_analyses': 0,
                    'app_start_time': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat()
                }
                logger.info("No stats file found, returning default stats")
                return default_stats
        except Exception as e:
            logger.error(f"Failed to load stats: {e}")
            return {}
    
    def save_analysis_history(self, history: List[Dict[str, Any]]):
        """Save analysis history."""
        try:
            # Keep only last 1000 analyses to prevent file from growing too large
            if len(history) > 1000:
                history = history[-1000:]
            
            with open(self.analysis_history_file, 'w') as f:
                json.dump(history, f, indent=2, default=str)
            logger.info(f"Saved {len(history)} analysis records to {self.analysis_history_file}")
        except Exception as e:
            logger.error(f"Failed to save analysis history: {e}")
    
    def load_analysis_history(self) -> List[Dict[str, Any]]:
        """Load analysis history."""
        try:
            if os.path.exists(self.analysis_history_file):
                with open(self.analysis_history_file, 'r') as f:
                    history = json.load(f)
                logger.info(f"Loaded {len(history)} analysis records from {self.analysis_history_file}")
                return history
            else:
                logger.info("No analysis history file found, returning empty list")
                return []
        except Exception as e:
            logger.error(f"Failed to load analysis history: {e}")
            return []
    
    def save_session_data(self, session_data: Dict[str, Any]):
        """Save session data using pickle for complex objects."""
        try:
            with open(self.session_data_file, 'wb') as f:
                pickle.dump(session_data, f)
            logger.info(f"Saved session data to {self.session_data_file}")
        except Exception as e:
            logger.error(f"Failed to save session data: {e}")
    
    def load_session_data(self) -> Dict[str, Any]:
        """Load session data."""
        try:
            if os.path.exists(self.session_data_file):
                with open(self.session_data_file, 'rb') as f:
                    session_data = pickle.load(f)
                logger.info(f"Loaded session data from {self.session_data_file}")
                return session_data
            else:
                logger.info("No session data file found, returning empty dict")
                return {}
        except Exception as e:
            logger.error(f"Failed to load session data: {e}")
            return {}
    
    def backup_data(self, backup_dir="backups"):
        """Create a backup of all data files."""
        try:
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_path)
            
            # Copy all data files
            files_to_backup = [
                self.users_file,
                self.stats_file,
                self.analysis_history_file,
                self.session_data_file
            ]
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    backup_file = os.path.join(backup_path, filename)
                    
                    with open(file_path, 'rb') as src, open(backup_file, 'wb') as dst:
                        dst.write(src.read())
            
            logger.info(f"Created backup at {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def cleanup_old_data(self, days_to_keep=30):
        """Clean up old analysis history and backups."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean up old analysis history
            history = self.load_analysis_history()
            filtered_history = [
                record for record in history
                if datetime.fromisoformat(record.get('timestamp', '1970-01-01')) > cutoff_date
            ]
            
            if len(filtered_history) != len(history):
                self.save_analysis_history(filtered_history)
                logger.info(f"Cleaned up {len(history) - len(filtered_history)} old analysis records")
            
            # Clean up old backups
            backup_dir = "backups"
            if os.path.exists(backup_dir):
                for backup_folder in os.listdir(backup_dir):
                    backup_path = os.path.join(backup_dir, backup_folder)
                    if os.path.isdir(backup_path):
                        folder_time = datetime.fromtimestamp(os.path.getctime(backup_path))
                        if folder_time < cutoff_date:
                            import shutil
                            shutil.rmtree(backup_path)
                            logger.info(f"Removed old backup: {backup_folder}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")

# Global instance for easy access
data_persistence = DataPersistence()

def get_data_persistence():
    """Get the global data persistence instance."""
    return data_persistence
