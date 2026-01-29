# Version: 0.02
import pandas as pd
import requests
import json
import os
import time
import logging
from typing import Optional, Tuple, Dict, Any

from .cache_manager import CacheManager
from .config import CACHE_SETTINGS, API_SETTINGS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErgastAPI:
    """Wrapper class for the Ergast F1 API with intelligent caching.
    
    Provides methods to fetch Formula 1 racing data including driver standings,
    constructor standings, race information, and results.
    
    Features:
    - Smart caching with metadata tracking
    - API call rate limiting
    - Schedule-aware refresh logic
    - Manual refresh capability
    
    Attributes:
        BASE_URL (str): Base URL for the Ergast F1 API
        cache_manager (CacheManager): Manages caching and metadata
    """
    
    BASE_URL = API_SETTINGS['base_url']
    
    def __init__(self, cache_dir='api/cache'):
        """Initialize API handler with cache manager.
        
        Args:
            cache_dir: Directory for cache files
        """
        self.cache_manager = CacheManager(cache_dir)
    
    def get_next_race(self, force_refresh: bool = False) -> Optional[Dict]:
        """Fetch the next upcoming F1 race information with intelligent caching.
        
        Args:
            force_refresh: Force API call even if cache is fresh
            
        Returns:
            Dictionary with race details or None if unavailable
        """
        cache_key = 'next_race'
        settings = CACHE_SETTINGS['next_race']
        
        # Step 1: Load from cache first (always try, even if expired)
        cached_data = self.cache_manager.load_cache(cache_key, max_age_seconds=None)
        
        # Step 2: Determine if we should refresh
        should_refresh = force_refresh or self.cache_manager.should_refresh(
            cache_key,
            settings['refresh_interval'],
            settings['max_api_calls_per_day'],
            force_refresh
        )
        
        # Step 3: Try API call if needed
        api_data = None
        if should_refresh:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/current/next.json",
                    timeout=API_SETTINGS['timeout']
                )
                response.raise_for_status()
                api_data = response.json()
                self.cache_manager.save_cache(cache_key, api_data)
                logger.info("Successfully fetched and cached next race data")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to retrieve the next race from API: {e}")
                if cached_data:
                    logger.info("Using cached next race data as fallback")
        
        # Step 4: Process data (prefer API, fallback to cache)
        data_to_process = api_data if api_data else cached_data
        
        if data_to_process:
            try:
                next_race = data_to_process['MRData']['RaceTable']['Races'][0]
                race_details = {
                    "name": next_race['raceName'],
                    "circuit": next_race['Circuit']['circuitName'],
                    "date": next_race['date'],
                    "time": next_race['time'],
                    "url": next_race['url'],
                    "location": f"{next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}"
                }
                return race_details
            except (KeyError, IndexError) as e:
                logger.error(f"Unexpected data structure in response: {e}")
                return None
        
        logger.warning("No next race data available from API or cache")
        return None

    def get_last_race(self, force_refresh: bool = False) -> Tuple[Optional[Dict], Optional[list]]:
        """Fetch the last completed F1 race information and podium results with intelligent caching.
        
        Args:
            force_refresh: Force API call even if cache is fresh
            
        Returns:
            Tuple of (race_details dict, podium list) or (None, None) if unavailable
        """
        cache_key = 'last_race'
        settings = CACHE_SETTINGS['last_race']
        
        # Step 1: Load from cache first (always try, even if expired)
        cached_data = self.cache_manager.load_cache(cache_key, max_age_seconds=None)
        
        # Step 2: Determine if we should refresh
        should_refresh = force_refresh or self.cache_manager.should_refresh(
            cache_key,
            settings['refresh_interval'],
            settings['max_api_calls_per_day'],
            force_refresh
        )
        
        # Step 3: Try API call if needed
        api_data = None
        if should_refresh:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/current/last/results.json",
                    timeout=API_SETTINGS['timeout']
                )
                response.raise_for_status()
                api_data = response.json()
                self.cache_manager.save_cache(cache_key, api_data)
                logger.info("Successfully fetched and cached last race data")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to retrieve the last race from API: {e}")
                if cached_data:
                    logger.info("Using cached last race data as fallback")
        
        # Step 4: Process data (prefer API, fallback to cache)
        data_to_process = api_data if api_data else cached_data
        
        if data_to_process:
            try:
                race_results = data_to_process['MRData']['RaceTable']['Races'][0]
                race_details = {
                    "name": race_results['raceName'],
                    "circuit": race_results['Circuit']['circuitName'],
                    "date": race_results['date'],
                    "location": f"{race_results['Circuit']['Location']['locality']}"
                }
                race_podium = race_results['Results'][0:3]
                podium = []
                for result in race_podium:
                    driver_card = {
                        "position": result['position'],
                        "name": f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
                        "number": result['Driver']['permanentNumber'],
                        "team": result['Constructor']['name'],
                        "code_Name": result['Driver']['code'],
                    }
                    podium.append(driver_card)
                return race_details, podium
            except (KeyError, IndexError) as e:
                logger.error(f"Unexpected data structure in response: {e}")
                return None, None
        
        logger.warning("No last race data available from API or cache")
        return None, None


            
        
    def get_driver_standings(self, force_refresh: bool = False) -> Optional[list]:
        """Fetch driver standings with intelligent caching.
        
        Args:
            force_refresh: Force API call even if cache is fresh
            
        Returns:
            List of processed driver standings or None if unavailable
        """
        cache_key = 'driver_standings'
        settings = CACHE_SETTINGS['driver_standings']
        
        # Step 1: Load from cache first (always try, even if expired)
        cached_data = self.cache_manager.load_cache(cache_key, max_age_seconds=None)
        
        # Step 2: Determine if we should refresh
        should_refresh = force_refresh or self.cache_manager.should_refresh(
            cache_key,
            settings['refresh_interval'],
            settings['max_api_calls_per_day'],
            force_refresh
        )
        
        # Step 3: Try API call if needed
        api_data = None
        if should_refresh:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/current/driverStandings.json",
                    timeout=API_SETTINGS['timeout']
                )
                response.raise_for_status()
                api_data = response.json()
                self.cache_manager.save_cache(cache_key, api_data)
                logger.info("Successfully fetched and cached driver standings")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to retrieve driver standings from API: {e}")
                if cached_data:
                    logger.info("Using cached driver standings as fallback")
        
        # Step 4: Process data (prefer API, fallback to cache)
        data_to_process = api_data if api_data else cached_data
        
        if data_to_process:
            processed_data = self.processed_standings(data_to_process)
            if processed_data:
                return processed_data
        
        logger.error("No driver standings data available to process")
        return None

    def processed_standings(self, data):
        """Process raw driver standings data into a structured format.
        
        Args:
            data (dict): Raw API response containing driver standings
            
        Returns:
            list: List of dictionaries containing processed driver information
        """
        raw_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        raw_standings = sorted(raw_standings, key=lambda x: int(x['position']))
        
        # Process the data to fit the UI component
        processed_standings = []
        for driver in raw_standings:
            driver_info = {
                'POS': int(driver['position']),
                'NAME': f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
                'NATIONALITY': driver['Driver']['nationality'],
                'TEAM': {
                    'name': driver['Constructors'][0]['name'], 
                    'teamId': driver['Constructors'][0]['constructorId']
                },
                'PTS': driver['points']
            }
            processed_standings.append(driver_info)
        return processed_standings
    

    def fetch_constructor_standings(self, season='current', force_refresh: bool = False) -> list:
        """Fetch constructor standings for a given season with intelligent caching.
        
        Args:
            season: F1 season year or 'current'
            force_refresh: Force API call even if cache is fresh
            
        Returns:
            List of constructor standings
            
        Raises:
            Exception: If no data available from API or cache
        """
        cache_key = f'constructor_standings_{season}'
        settings = CACHE_SETTINGS['constructor_standings']
        
        # Step 1: Load from cache first (always try, even if expired)
        cached_data = self.cache_manager.load_cache(cache_key, max_age_seconds=None)
        
        # Step 2: Determine if we should refresh
        should_refresh = force_refresh or self.cache_manager.should_refresh(
            cache_key,
            settings['refresh_interval'],
            settings['max_api_calls_per_day'],
            force_refresh
        )
        
        # Step 3: Try API call if needed
        api_data = None
        if should_refresh:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/{season}/constructorStandings.json",
                    timeout=API_SETTINGS['timeout']
                )
                response.raise_for_status()
                api_data = response.json()
                self.cache_manager.save_cache(cache_key, api_data)
                logger.info("Successfully fetched and cached constructor standings")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch constructor standings from API: {e}")
                if cached_data:
                    logger.info("Using cached constructor standings as fallback")
        
        # Step 4: Process data (prefer API, fallback to cache)
        data_to_process = api_data if api_data else cached_data
        
        if data_to_process:
            try:
                standings = data_to_process['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
                return standings
            except (KeyError, IndexError) as e:
                logger.error(f"Unexpected data structure in API response: {e}")
                if cached_data:
                    raise Exception(f"Failed to process cached data: {e}") from e
                raise Exception(f"Failed to fetch data: {e}") from e
        
        raise Exception("No constructor standings data available from API or cache")
    
    def process_constructors_standings(self, standings):
        """Process raw constructor standings data into a pandas DataFrame.
        
        Args:
            standings (list): Raw constructor standings data from API
            
        Returns:
            pd.DataFrame: DataFrame containing processed constructor standings
        """
        data = []
        for item in standings:
            constructor = item['Constructor']['name']
            points = item['points']
            wins = item['wins']
            position = item['position']
            data.append({
                'Position': position,
                'Constructor': constructor,
                'Wins': wins,
                'Points': points
            })
        return pd.DataFrame(data)
    
    def get_constructors_championship(self, force_refresh: bool = False):
        """Fetch and process constructor championship standings.
        
        Args:
            force_refresh: Force API call even if cache is fresh
            
        Returns:
            pd.DataFrame: DataFrame containing constructor standings with
                Position, Constructor, Points, and Wins columns
        """
        standings = self.fetch_constructor_standings(force_refresh=force_refresh)
        return self.process_constructors_standings(standings)
    
    def refresh_all_data(self):
        """Manually refresh all cached data by forcing API calls.
        
        This method bypasses cache checks and fetches fresh data from the API
        for all endpoints. Use sparingly to respect API rate limits.
        """
        logger.info("Manually refreshing all data...")
        try:
            self.get_next_race(force_refresh=True)
            self.get_last_race(force_refresh=True)
            self.get_driver_standings(force_refresh=True)
            self.get_constructors_championship(force_refresh=True)
            logger.info("All data refreshed successfully")
        except Exception as e:
            logger.error(f"Error during manual refresh: {e}")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get status information about cached data.
        
        Returns:
            Dictionary with cache status for each endpoint
        """
        status = {}
        cache_keys = ['next_race', 'last_race', 'driver_standings', 'constructor_standings_current']
        
        for key in cache_keys:
            last_update = self.cache_manager.get_last_update_time(key)
            call_count = self.cache_manager.get_api_call_count(key)
            has_cache = self.cache_manager.load_cache(key) is not None
            
            status[key] = {
                'has_cache': has_cache,
                'last_update': last_update.isoformat() if last_update else None,
                'api_calls': call_count
            }
        
        return status
