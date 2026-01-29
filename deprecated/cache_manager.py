"""
Cache Manager for F1 Data

Provides intelligent caching with:
- Metadata tracking (last update, API call counts)
- Smart cache invalidation based on F1 schedule
- Manual refresh controls
- API call rate limiting
"""

import json
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching with metadata tracking and smart invalidation."""
    
    def __init__(self, cache_dir='api/cache'):
        """Initialize cache manager.
        
        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = cache_dir
        self.metadata_file = os.path.join(cache_dir, 'cache_metadata.json')
        self._ensure_cache_dir()
        self._load_metadata()
    
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist."""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _load_metadata(self):
        """Load cache metadata from file."""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {
                    'api_calls': {},
                    'last_updates': {},
                    'cache_settings': {}
                }
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading metadata: {e}. Creating new metadata.")
            self.metadata = {
                'api_calls': {},
                'last_updates': {},
                'cache_settings': {}
            }
    
    def _save_metadata(self):
        """Save metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def get_cache_path(self, cache_key: str) -> str:
        """Get file path for a cache key.
        
        Args:
            cache_key: Unique identifier for the cache entry
            
        Returns:
            Full path to cache file
        """
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def load_cache(self, cache_key: str, max_age_seconds: Optional[int] = None) -> Optional[Dict]:
        """Load data from cache if it exists and is fresh.
        
        Args:
            cache_key: Unique identifier for the cache entry
            max_age_seconds: Maximum age in seconds (None = always valid if exists)
            
        Returns:
            Cached data or None if not available/expired
        """
        cache_path = self.get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
        
        # Check if cache is expired
        if max_age_seconds is not None:
            file_mod_time = os.path.getmtime(cache_path)
            current_time = time.time()
            if (current_time - file_mod_time) > max_age_seconds:
                logger.debug(f"Cache expired for {cache_key}")
                return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            logger.debug(f"Loaded cache for {cache_key}")
            return data
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error reading cache file {cache_key}: {e}")
            return None
    
    def save_cache(self, cache_key: str, data: Dict, force_refresh: bool = False):
        """Save data to cache and update metadata.
        
        Args:
            cache_key: Unique identifier for the cache entry
            data: Data to cache
            force_refresh: If True, bypass checks and force save
        """
        cache_path = self.get_cache_path(cache_key)
        
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Update metadata
            self.metadata['last_updates'][cache_key] = time.time()
            if cache_key not in self.metadata['api_calls']:
                self.metadata['api_calls'][cache_key] = 0
            self.metadata['api_calls'][cache_key] += 1
            
            self._save_metadata()
            logger.info(f"Cached data for {cache_key}")
        except IOError as e:
            logger.error(f"Failed to save cache for {cache_key}: {e}")
    
    def should_refresh(self, cache_key: str, refresh_interval: int, 
                      max_api_calls_per_day: Optional[int] = None,
                      force_refresh: bool = False) -> bool:
        """Determine if cache should be refreshed.
        
        Args:
            cache_key: Unique identifier for the cache entry
            refresh_interval: Minimum seconds between refreshes
            max_api_calls_per_day: Maximum API calls per day (None = unlimited)
            force_refresh: Force refresh regardless of other conditions
            
        Returns:
            True if cache should be refreshed
        """
        if force_refresh:
            return True
        
        # Check if cache exists
        cache_path = self.get_cache_path(cache_key)
        if not os.path.exists(cache_path):
            return True
        
        # Check refresh interval
        last_update = self.metadata['last_updates'].get(cache_key, 0)
        current_time = time.time()
        if (current_time - last_update) < refresh_interval:
            return False
        
        # Check API call limits
        if max_api_calls_per_day is not None:
            calls_today = self._get_calls_today(cache_key)
            if calls_today >= max_api_calls_per_day:
                logger.warning(f"API call limit reached for {cache_key} ({calls_today}/{max_api_calls_per_day})")
                return False
        
        return True
    
    def _get_calls_today(self, cache_key: str) -> int:
        """Get number of API calls made today for a cache key."""
        # This is simplified - in production, you'd track calls per day
        # For now, we'll use a simple counter that resets daily
        last_update = self.metadata['last_updates'].get(cache_key, 0)
        if time.time() - last_update > 86400:  # More than 24 hours ago
            return 0
        return self.metadata['api_calls'].get(cache_key, 0)
    
    def get_last_update_time(self, cache_key: str) -> Optional[datetime]:
        """Get when cache was last updated.
        
        Args:
            cache_key: Unique identifier for the cache entry
            
        Returns:
            datetime of last update or None
        """
        timestamp = self.metadata['last_updates'].get(cache_key)
        if timestamp:
            return datetime.fromtimestamp(timestamp)
        return None
    
    def get_api_call_count(self, cache_key: str) -> int:
        """Get total API call count for a cache key."""
        return self.metadata['api_calls'].get(cache_key, 0)
    
    def is_race_weekend(self, race_date: Optional[str] = None) -> bool:
        """Check if we're in a race weekend period.
        
        Race weekends typically run Friday-Sunday. Data should refresh:
        - Friday morning (practice starts)
        - Sunday evening (race ends)
        - Monday morning (final results available)
        
        Args:
            race_date: Race date string (YYYY-MM-DD) or None to check current date
            
        Returns:
            True if we're in a race weekend period
        """
        if race_date:
            try:
                race_dt = datetime.strptime(race_date, '%Y-%m-%d')
            except ValueError:
                return False
        else:
            race_dt = datetime.now()
        
        # Simplified: consider Friday-Sunday as race weekend
        # In production, you'd check actual race calendar
        weekday = race_dt.weekday()  # 0=Monday, 6=Sunday
        return weekday >= 4  # Friday, Saturday, or Sunday
    
    def should_refresh_based_on_schedule(self, cache_key: str, 
                                        race_date: Optional[str] = None,
                                        refresh_interval: int = 86400) -> bool:
        """Smart refresh based on F1 schedule.
        
        Refresh logic:
        - Race weekends: Refresh every 6 hours
        - Non-race weekends: Refresh every 24 hours
        - After race date: Refresh more frequently (results available)
        
        Args:
            cache_key: Cache identifier
            race_date: Next/Last race date (YYYY-MM-DD)
            refresh_interval: Default refresh interval in seconds
            
        Returns:
            True if should refresh based on schedule
        """
        # Check basic refresh interval first
        if not self.should_refresh(cache_key, refresh_interval):
            return False
        
        # If we have race date, use smarter logic
        if race_date:
            try:
                race_dt = datetime.strptime(race_date, '%Y-%m-%d')
                now = datetime.now()
                days_until_race = (race_dt - now).days
                
                # Very close to race (within 3 days): refresh more often
                if -1 <= days_until_race <= 3:
                    return self.should_refresh(cache_key, 21600)  # 6 hours
                
                # Just after race (within 7 days): refresh daily
                if -7 <= days_until_race < -1:
                    return self.should_refresh(cache_key, 86400)  # 24 hours
                
                # Far from race: refresh weekly
                return self.should_refresh(cache_key, 604800)  # 7 days
            except ValueError:
                pass
        
        # Default behavior
        return self.should_refresh(cache_key, refresh_interval)
    
    def clear_cache(self, cache_key: Optional[str] = None):
        """Clear cache for a specific key or all caches.
        
        Args:
            cache_key: Specific cache to clear (None = clear all)
        """
        if cache_key:
            cache_path = self.get_cache_path(cache_key)
            if os.path.exists(cache_path):
                os.remove(cache_path)
                if cache_key in self.metadata['last_updates']:
                    del self.metadata['last_updates'][cache_key]
                logger.info(f"Cleared cache for {cache_key}")
        else:
            # Clear all caches
            for file in os.listdir(self.cache_dir):
                if file.endswith('.json') and file != 'cache_metadata.json':
                    os.remove(os.path.join(self.cache_dir, file))
            self.metadata['last_updates'] = {}
            logger.info("Cleared all caches")
        
        self._save_metadata()
