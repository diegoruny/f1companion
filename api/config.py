"""
Configuration settings for F1 API data management
"""

# Cache settings (in seconds)
CACHE_SETTINGS = {
    'driver_standings': {
        'refresh_interval': 86400,  # 24 hours
        'max_age': 604800,  # 7 days max age
        'max_api_calls_per_day': 10
    },
    'constructor_standings': {
        'refresh_interval': 86400,  # 24 hours
        'max_age': 604800,  # 7 days max age
        'max_api_calls_per_day': 10
    },
    'next_race': {
        'refresh_interval': 86400,  # 24 hours
        'max_age': 604800,  # 7 days max age
        'max_api_calls_per_day': 5
    },
    'last_race': {
        'refresh_interval': 86400,  # 24 hours
        'max_age': 604800,  # 7 days max age
        'max_api_calls_per_day': 5
    }
}

# API settings
API_SETTINGS = {
    'base_url': 'http://ergast.com/api/f1',
    'timeout': 5,
    'max_retries': 2
}

# Global API call limits
GLOBAL_API_LIMITS = {
    'max_calls_per_day': 50,
    'max_calls_per_hour': 10
}
