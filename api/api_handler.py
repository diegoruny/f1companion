# Version: 0.01
import pandas as pd
import requests
import json
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErgastAPI:
    """Wrapper class for the Ergast F1 API.
    
    Provides methods to fetch Formula 1 racing data including driver standings,
    constructor standings, race information, and results.
    
    Attributes:
        BASE_URL (str): Base URL for the Ergast F1 API
    """
    BASE_URL = "http://ergast.com/api/f1"
    
    def get_next_race(self):
        """Fetch the next upcoming F1 race information."""
        try:
            response = requests.get(f"{self.BASE_URL}/current/next.json", timeout=5)
            response.raise_for_status()
            data = response.json()
            next_race = data['MRData']['RaceTable']['Races'][0]
            
            race_details = {
                "name": next_race['raceName'],
                "circuit": next_race['Circuit']['circuitName'],
                "date": next_race['date'],
                "time": next_race['time'],
                "url": next_race['url'],
                "location": f"{next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}"
            }
            return race_details
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve the next race: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected data structure in API response: {e}")
            return None

    def get_last_race(self):
        """Fetch the last completed F1 race information and podium results."""
        try:
            response = requests.get(f"{self.BASE_URL}/current/last/results.json", timeout=5)
            response.raise_for_status()
            data = response.json()
            race_results = data['MRData']['RaceTable']['Races'][0]
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
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve the last race: {e}")
            return None, None
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected data structure in API response: {e}")
            return None, None


            
        
    def get_driver_standings(self, CACHE_PATH='current_drivers_standings.json', cache_timeout=3600):
        """Fetch driver standings with caching support."""
        data = None
        
        # Check if cache file exists and is not too old
        try:
            if os.path.exists(CACHE_PATH):
                file_mod_time = os.path.getmtime(CACHE_PATH)
                current_time = time.time()
                if (current_time - file_mod_time) < cache_timeout:
                    with open(CACHE_PATH, 'r') as file:
                        data = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error reading cache file: {e}. Fetching fresh data.")
        
        if not data:
            try:
                response = requests.get(f"{self.BASE_URL}/current/driverStandings.json", timeout=5)
                response.raise_for_status()
                data = response.json()
                # Cache Data
                try:
                    with open(CACHE_PATH, 'w') as file:
                        json.dump(data, file)
                except IOError as e:
                    logger.warning(f"Failed to write cache file: {e}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to retrieve driver standings: {e}")
                return None
        
        if data:
            processed_data = self.processed_standings(data)
            if processed_data:
                return processed_data
        
        logger.error("No data available to process")
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
    

    def fetch_constructor_standings(self, season='current'):
        """Fetch constructor standings for a given season."""
        try:
            response = requests.get(f"{self.BASE_URL}/{season}/constructorStandings.json", timeout=5)
            response.raise_for_status()
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            return standings
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch constructor standings: {e}")
            raise Exception(f"Failed to fetch data: {e}") from e
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected data structure in API response: {e}")
            raise Exception(f"Unexpected API response structure: {e}") from e
    
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
    def get_constructors_championship(self):
        """Fetch and process constructor championship standings.
        
        Returns:
            pd.DataFrame: DataFrame containing constructor standings with
                Position, Constructor, Points, and Wins columns
        """
        standings = self.fetch_constructor_standings()
        return self.process_constructors_standings(standings)
