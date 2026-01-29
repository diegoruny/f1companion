"""Configuration settings for F1 Companion application.

This module centralizes all configuration values used across the application.
Modify these settings to customize behavior without changing code.
"""

import os
from pathlib import Path

# ============================================================================
# Project Paths
# ============================================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data file locations (CSV/JSON offline mode)
DATA_PATHS = {
    'race_data': PROJECT_ROOT / 'final_race_data.csv',
    'driver_standings': PROJECT_ROOT / 'api' / 'current_drivers_standings.json',
    'constructor_standings': PROJECT_ROOT / 'api' / 'current_constructor_standings.json',
}

# ============================================================================
# API Settings (Legacy - Ergast API is offline)
# ============================================================================

# These settings are preserved for future API integrations
# See deprecated/api_handler.py for reference implementation
LEGACY_API_SETTINGS = {
    'base_url': 'http://ergast.com/api/f1',
    'timeout': 5,
    'max_retries': 2
}

# ============================================================================
# Cache Settings (Legacy - not used in CSV-only mode)
# ============================================================================

LEGACY_CACHE_SETTINGS = {
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

# ============================================================================
# Application Settings
# ============================================================================

APP_SETTINGS = {
    'theme': 'darkly',  # ttkbootstrap theme
    'window_title': 'F1 Companion',
    'window_geometry': '1200x800',
}

# ============================================================================
# Data Display Settings
# ============================================================================

DISPLAY_SETTINGS = {
    'max_drivers_shown': 20,
    'max_constructors_shown': 10,
    'date_format': '%Y-%m-%d',
}

# ============================================================================
# Usage Notes
# ============================================================================

# To use these paths in your code:
#
#   from config import DATA_PATHS, PROJECT_ROOT
#
#   race_data_path = str(DATA_PATHS['race_data'])
#   standings_path = str(DATA_PATHS['driver_standings'])
#
# This replaces hardcoded paths like:
#   os.path.join(os.path.dirname(__file__), 'final_race_data.csv')

