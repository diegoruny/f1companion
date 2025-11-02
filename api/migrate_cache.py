"""
Migration script to move existing cache files to new cache structure.

This script migrates old cache files from api/ directory to api/cache/ directory
and updates them to use the new cache key naming convention.
"""

import os
import json
import shutil
from pathlib import Path

def migrate_cache_files():
    """Migrate old cache files to new structure."""
    api_dir = Path('api')
    cache_dir = Path('api/cache')
    
    # Create cache directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Mapping of old cache files to new cache keys
    migrations = {
        'current_drivers_standings.json': 'driver_standings.json',
        'current_constructor_standings.json': 'constructor_standings_current.json',
        'current_next_race.json': 'next_race.json',
        'current_last_race.json': 'last_race.json'
    }
    
    migrated_count = 0
    
    # Migrate files from api directory
    for old_file, new_file in migrations.items():
        old_path = api_dir / old_file
        new_path = cache_dir / new_file
        
        if old_path.exists() and not new_path.exists():
            try:
                # Copy file to new location
                shutil.copy2(old_path, new_path)
                print(f"[OK] Migrated {old_file} -> cache/{new_file}")
                migrated_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to migrate {old_file}: {e}")
    
    # Also check root directory for cache files
    root_dir = Path('.')
    root_migrations = {
        'current_drivers_standings.json': 'driver_standings.json'
    }
    
    for old_file, new_file in root_migrations.items():
        old_path = root_dir / old_file
        new_path = cache_dir / new_file
        
        if old_path.exists() and not new_path.exists():
            try:
                shutil.copy2(old_path, new_path)
                print(f"[OK] Migrated {old_file} (root) -> cache/{new_file}")
                migrated_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to migrate {old_file}: {e}")
    
    print(f"\nMigration complete: {migrated_count} file(s) migrated")
    print(f"Cache files are now in: {cache_dir.absolute()}")

if __name__ == '__main__':
    migrate_cache_files()
