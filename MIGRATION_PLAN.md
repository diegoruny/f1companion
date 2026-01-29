# F1 Companion - API Migration Plan

> **From:** Ergast API (DEAD ☠️)
> **To:** OpenF1 API (https://openf1.org)
> **Estimated Time:** 2-3 hours

---

## API Comparison

### Ergast (Old - Dead)
```
https://ergast.com/api/f1/current/driverStandings.json
https://ergast.com/api/f1/current/next.json
https://ergast.com/api/f1/current/last/results.json
```

### OpenF1 (New - Active)
```
https://api.openf1.org/v1/drivers?session_key=latest
https://api.openf1.org/v1/sessions?year=2026
https://api.openf1.org/v1/position?session_key=latest
```

---

## Current Functionality to Migrate

| Feature | Ergast Endpoint | OpenF1 Equivalent |
|---------|-----------------|-------------------|
| Driver List | `/current/drivers.json` | `/v1/drivers?session_key=latest` |
| Driver Standings | `/current/driverStandings.json` | ⚠️ Not directly available* |
| Constructor Standings | `/current/constructorStandings.json` | ⚠️ Not directly available* |
| Next Race | `/current/next.json` | `/v1/sessions?year=2026` (filter future) |
| Last Race Results | `/current/last/results.json` | `/v1/position?session_key=latest` |

*OpenF1 focuses on telemetry/live data. Standings may need secondary source or calculation.

---

## Files to Modify

### 1. `api/config.py`
```python
# OLD
API_SETTINGS = {
    'base_url': 'https://ergast.com/api/f1',
    ...
}

# NEW
API_SETTINGS = {
    'base_url': 'https://api.openf1.org/v1',
    'timeout': 10,
    'retry_attempts': 3,
}
```

### 2. `api/api_handler.py` (Main Work)

Replace all Ergast-specific methods:

```python
# OLD
def get_next_race(self):
    response = requests.get(f"{self.BASE_URL}/current/next.json")
    ...

# NEW
def get_next_race(self):
    """Get next scheduled session from OpenF1."""
    response = requests.get(
        f"{self.BASE_URL}/sessions",
        params={'year': datetime.now().year}
    )
    sessions = response.json()
    # Filter for future sessions
    now = datetime.now(timezone.utc)
    future = [s for s in sessions if datetime.fromisoformat(s['date_start']) > now]
    return future[0] if future else None
```

### 3. Data Model Changes

Ergast response structure → OpenF1 structure:

```python
# Ergast driver
{
    "driverId": "verstappen",
    "givenName": "Max",
    "familyName": "Verstappen",
    "nationality": "Dutch"
}

# OpenF1 driver
{
    "driver_number": 1,
    "full_name": "Max VERSTAPPEN",
    "name_acronym": "VER",
    "team_name": "Red Bull Racing",
    "team_colour": "4781D7",
    "headshot_url": "https://..."
}
```

---

## Migration Steps

### Step 1: Update Config (5 min)
- [ ] Change `base_url` in `api/config.py`
- [ ] Update timeout/retry settings

### Step 2: Create OpenF1 Adapter (45 min)
- [ ] Create new `api/openf1_handler.py`
- [ ] Implement `get_drivers()` 
- [ ] Implement `get_sessions()` (replaces next_race)
- [ ] Implement `get_positions()` (for race results)

### Step 3: Handle Missing Data (30 min)
- [ ] Driver/Constructor standings not in OpenF1
- [ ] Option A: Use cached CSV data (already exists)
- [ ] Option B: Add secondary API (f1api.dev or scrape)
- [ ] Option C: Remove standings feature temporarily

### Step 4: Update UI Mappings (30 min)
- [ ] `ui/list_builder.py` - Update field names
- [ ] `ui/constructors_standings.py` - May need rework
- [ ] `ui/next_race.py` - Update data structure

### Step 5: Update Cache Keys (15 min)
- [ ] `api/cache_manager.py` - Update cache key names
- [ ] Clear old cache files

### Step 6: Test (30 min)
- [ ] Test each endpoint manually
- [ ] Verify UI displays correctly
- [ ] Check cache behavior

---

## OpenF1 API Reference

### Drivers
```bash
curl "https://api.openf1.org/v1/drivers?session_key=latest"
```

### Sessions (Schedule)
```bash
curl "https://api.openf1.org/v1/sessions?year=2026"
```

### Positions (Race Results)
```bash
curl "https://api.openf1.org/v1/position?session_key=latest"
```

### Laps (Timing Data)
```bash
curl "https://api.openf1.org/v1/laps?session_key=latest&driver_number=1"
```

---

## Fallback Strategy

If OpenF1 doesn't have standings data:

1. **Use CSV data** - Already have `final_race_data.csv` and `current_drivers_standings.json`
2. **Static 2025 season data** - Show historical data as demo
3. **Add f1api.dev** - Secondary API for standings

---

## Post-Migration Checklist

- [ ] README updated with new API info
- [ ] Old Ergast references removed
- [ ] Cache files cleared
- [ ] Test on Windows (Tkinter)
- [ ] Commit with descriptive message

---

## Commands to Start

```bash
cd ~/projects/f1companion
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test OpenF1 connection
python3 -c "import requests; print(requests.get('https://api.openf1.org/v1/drivers?session_key=latest').json()[0])"
```

---

*Plan created by Jarvis | Ready for execution*
