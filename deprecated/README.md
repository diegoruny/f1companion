# Deprecated Code Archive

This directory contains code that is no longer actively used but preserved for reference.

## API Layer (Offline Migration)

### `api_handler.py` (391 lines)
- **Original Purpose:** Live API integration with Ergast F1 API
- **Deprecated Date:** 2026-01-29
- **Reason:** Ergast API went offline; replaced by `csv_handler.py` (offline CSV mode)
- **Keep Because:** Reference implementation, may be useful for future API integrations

### `cache_manager.py` (131 lines)
- **Original Purpose:** Cache management for live API responses
- **Deprecated Date:** 2026-01-29
- **Reason:** No longer needed without live API
- **Keep Because:** Sophisticated caching patterns, may be reused

### `migrate_cache.py` (36 lines)
- **Original Purpose:** Migrate cache format between versions
- **Deprecated Date:** 2026-01-29
- **Reason:** No longer relevant without live API/cache
- **Keep Because:** Migration pattern reference

### `config.py` (API config)
- **Original Purpose:** API cache settings and rate limits
- **Deprecated Date:** 2026-01-29
- **Reason:** Replaced by root-level `config.py` with centralized paths
- **Keep Because:** Reference for cache configuration patterns

---

## Experimental Code

### `experimental/` directory
- **Contents:** Old prototypes (driver_standings.py, test_api.py, turtle_sim.py)
- **Deprecated Date:** 2026-01-29
- **Reason:** Never integrated, outdated
- **Keep Because:** May contain useful ideas for future features

See `experimental/README.md` for details.

---

## Should I Delete These?

**Not yet.** Keep them until:
1. CSV-only mode proven stable in production (3+ months)
2. No plans to reintegrate live APIs
3. Code patterns have been extracted/documented elsewhere

If you need API integration again, start here instead of from scratch.

---

*Archived by Jarvis • 2026-01-29*

