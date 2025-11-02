# Smart Data Management System - Architecture Overview

## Overview

The F1 Companion app now uses an intelligent data management system that significantly reduces API calls while ensuring data freshness. The system implements smart caching, rate limiting, and schedule-aware refresh logic.

## Key Features

### 1. **Intelligent Caching System**
- **CacheManager**: Centralized cache management with metadata tracking
- **Metadata Tracking**: Tracks last update times and API call counts
- **Automatic Fallback**: Always loads from cache first, falls back to cache if API fails
- **Persistent Storage**: Cache files stored in `api/cache/` directory

### 2. **Smart Refresh Logic**
- **Time-based Refresh**: Configurable refresh intervals per endpoint
- **Schedule-aware**: Adapts refresh frequency based on F1 calendar:
  - Race weekends (within 3 days): Refresh every 6 hours
  - Post-race (within 7 days): Refresh daily
  - Off-season: Refresh weekly
- **Rate Limiting**: Prevents excessive API calls with per-endpoint limits

### 3. **API Call Management**
- **Per-endpoint Limits**: Configurable daily limits for each endpoint
  - Driver Standings: 10 calls/day
  - Constructor Standings: 10 calls/day
  - Next Race: 5 calls/day
  - Last Race: 5 calls/day
- **Global Limits**: 50 calls/day total, 10 calls/hour
- **Automatic Tracking**: Tracks API calls and prevents exceeding limits

### 4. **Manual Refresh Control**
- **Refresh Button**: UI button to manually refresh all data
- **Force Refresh**: `force_refresh=True` parameter bypasses cache checks
- **Status Display**: Shows last update time and cache status

## Architecture

### Components

```
api/
├── api_handler.py          # Main API wrapper with caching logic
├── cache_manager.py        # Cache management and metadata tracking
├── config.py               # Configuration settings
└── cache/                  # Cache storage directory
    ├── cache_metadata.json # Metadata tracking file
    ├── driver_standings.json
    ├── constructor_standings_current.json
    ├── next_race.json
    └── last_race.json
```

### Data Flow

1. **Request Data**
   ```
   User Request → API Handler → Cache Manager
   ```

2. **Cache Check**
   ```
   Cache Manager → Check Cache → Load if exists
   ```

3. **Refresh Decision**
   ```
   Cache Manager → Check Refresh Rules → API Call if needed
   ```

4. **Fallback**
   ```
   API Failure → Use Cached Data → Return to User
   ```

## Configuration

### Cache Settings (`api/config.py`)

```python
CACHE_SETTINGS = {
    'driver_standings': {
        'refresh_interval': 86400,      # 24 hours
        'max_age': 604800,              # 7 days max age
        'max_api_calls_per_day': 10
    },
    # ... other endpoints
}
```

### Customization

You can adjust cache behavior by modifying `api/config.py`:

- **Refresh Interval**: How often to check for updates
- **Max Age**: Maximum age before cache is considered stale
- **API Call Limits**: Maximum calls per day per endpoint

## Usage Examples

### Basic Usage (Automatic Caching)

```python
api_handler = ErgastAPI()

# Automatically uses cache if fresh, calls API if needed
next_race = api_handler.get_next_race()
driver_standings = api_handler.get_driver_standings()
```

### Manual Refresh

```python
# Force refresh all data
api_handler.refresh_all_data()

# Force refresh specific endpoint
next_race = api_handler.get_next_race(force_refresh=True)
```

### Check Cache Status

```python
status = api_handler.get_cache_status()
# Returns: {'driver_standings': {'has_cache': True, 'last_update': '...', 'api_calls': 5}, ...}
```

## Benefits

### Efficiency
- **Reduced API Calls**: Only calls API when necessary
- **Faster Load Times**: Instant display from cache
- **Offline Support**: Works with cached data when API unavailable

### Reliability
- **Automatic Fallback**: Always returns data if cache exists
- **Error Handling**: Gracefully handles API failures
- **Rate Limit Protection**: Prevents API abuse

### User Experience
- **Instant Display**: Cache loads immediately
- **Background Updates**: Updates happen in background
- **Manual Control**: User can force refresh when needed

## Migration from Old System

Old cache files are automatically migrated to the new structure:

- `api/current_drivers_standings.json` → `api/cache/driver_standings.json`
- `api/current_constructor_standings.json` → `api/cache/constructor_standings_current.json`

Run `python api/migrate_cache.py` to migrate existing files.

## Future Enhancements

1. **Schedule-aware Refresh**: Integrate F1 calendar for smarter refresh timing
2. **Background Updates**: Automatic background refresh during app idle
3. **Cache Warming**: Pre-fetch data before race weekends
4. **Analytics**: Track cache hit rates and API usage patterns

## Monitoring

The system logs all cache operations:
- Cache hits/misses
- API calls made
- Refresh decisions
- Error conditions

Check logs for detailed information about cache behavior.
