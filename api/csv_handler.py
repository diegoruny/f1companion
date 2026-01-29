"""CSV Data Handler for F1 Race Companion

Provides offline data access using local CSV/JSON files instead of live API.
This enables the app to work without internet connection.
"""

import json
import os
import pandas as pd
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime


class CSVDataHandler:
    """Handler for loading F1 data from local CSV and JSON files.
    
    Replaces ErgastAPI for offline operation with cached/static data.
    """
    
    def __init__(self, data_dir: str = None):
        """Initialize with data directory path.
        
        Args:
            data_dir: Directory containing CSV/JSON data files.
                     Defaults to project root.
        """
        if data_dir is None:
            # Default to project root
            data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.data_dir = data_dir
        self.race_data_path = os.path.join(data_dir, 'final_race_data.csv')
        self.standings_path = os.path.join(data_dir, 'current_drivers_standings.json')
        
        # Cache loaded data
        self._race_data: Optional[pd.DataFrame] = None
        self._standings_data: Optional[Dict] = None
    
    def _load_race_data(self) -> pd.DataFrame:
        """Load race data from CSV file."""
        if self._race_data is None:
            self._race_data = pd.read_csv(self.race_data_path)
        return self._race_data
    
    def _load_standings_data(self) -> Dict:
        """Load standings data from JSON file."""
        if self._standings_data is None:
            with open(self.standings_path, 'r') as f:
                self._standings_data = json.load(f)
        return self._standings_data
    
    def get_driver_standings(self) -> List[Dict[str, Any]]:
        """Get current driver championship standings.
        
        Returns format expected by UI:
        - POS: position number
        - NAME: "FirstName LastName"
        - NATIONALITY: driver nationality
        - TEAM: {'name': team_name, 'teamId': team_id}
        - PTS: points as string
        """
        data = self._load_standings_data()
        
        try:
            standings_list = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            
            result = []
            for standing in standings_list:
                driver = standing['Driver']
                constructor = standing['Constructors'][0] if standing['Constructors'] else {}
                
                # Format matching UI expectations (list_builder.py)
                result.append({
                    'POS': int(standing['position']),
                    'NAME': f"{driver.get('givenName', '')} {driver.get('familyName', '')}",
                    'NATIONALITY': driver.get('nationality', 'N/A'),
                    'TEAM': {
                        'name': constructor.get('name', 'N/A'),
                        'teamId': constructor.get('constructorId', 'N/A')
                    },
                    'PTS': standing['points'],
                    # Extra fields for compatibility
                    'CODE': driver.get('code', 'N/A'),
                    'NUMBER': driver.get('permanentNumber', 'N/A'),
                    'WINS': int(standing['wins']),
                })
            
            return result
        except (KeyError, IndexError) as e:
            print(f"Error parsing standings data: {e}")
            return []
    
    def get_constructor_standings(self) -> pd.DataFrame:
        """Get constructor championship standings as DataFrame.
        
        Returns:
            DataFrame with columns: Position, Constructor, Points, Wins
        """
        data = self._load_standings_data()
        
        try:
            standings_list = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            
            # Aggregate by team
            team_data: Dict[str, Dict] = {}
            for standing in standings_list:
                constructor = standing['Constructors'][0] if standing['Constructors'] else {}
                team_name = constructor.get('name', 'N/A')
                
                if team_name not in team_data:
                    team_data[team_name] = {
                        'Constructor': team_name,
                        'Points': 0,
                        'Wins': 0,
                    }
                team_data[team_name]['Points'] += float(standing['points'])
                team_data[team_name]['Wins'] += int(standing['wins'])
            
            # Sort by points and add positions
            sorted_teams = sorted(team_data.values(), key=lambda x: x['Points'], reverse=True)
            for i, team in enumerate(sorted_teams, 1):
                team['Position'] = i
            
            return pd.DataFrame(sorted_teams)[['Position', 'Constructor', 'Points', 'Wins']]
        except (KeyError, IndexError) as e:
            print(f"Error parsing constructor standings: {e}")
            return pd.DataFrame(columns=['Position', 'Constructor', 'Points', 'Wins'])
    
    def get_race_results(self, race_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get race results.
        
        Args:
            race_id: Specific race ID, or None for latest race.
            
        Returns:
            List of race results with driver positions, times, etc.
        """
        df = self._load_race_data()
        
        if race_id is None:
            # Get latest race (highest raceId)
            race_id = df['raceId'].max()
        
        race_df = df[df['raceId'] == race_id].copy()
        
        # Get unique driver results (first occurrence per driver)
        race_df = race_df.drop_duplicates(subset=['driverId'], keep='first')
        race_df = race_df.sort_values('positionOrder')
        
        results = []
        for _, row in race_df.iterrows():
            results.append({
                'position': int(row['positionOrder']),
                'driver_code': row['code'],
                'driver_name': f"{row['forename']} {row['surname']}",
                'team': row['name_x'],  # Constructor name
                'time': row.get('time_x', 'N/A'),
                'points': float(row['points']),
                'status': row.get('status', 'Finished'),
                'fastest_lap': row.get('fastestLapTime', 'N/A'),
                'grid': int(row['grid']),
            })
        
        return results
    
    def get_circuits(self) -> List[Dict[str, Any]]:
        """Get list of circuits from race data.
        
        Returns:
            List of unique circuits with location info.
        """
        df = self._load_race_data()
        
        circuits = df[['circuitRef', 'name_y', 'location', 'country', 'lat', 'lng']].drop_duplicates()
        
        return [
            {
                'circuit_id': row['circuitRef'],
                'name': row['name_y'],
                'location': row['location'],
                'country': row['country'],
                'lat': row['lat'],
                'lng': row['lng'],
            }
            for _, row in circuits.iterrows()
        ]
    
    def get_next_race(self) -> Optional[Dict[str, Any]]:
        """Get next race info.
        
        Note: With static data, returns info about a sample future race
        or the last race in the dataset as a placeholder.
        
        Returns:
            Race info dict with keys: name, circuit, location, date, time
        """
        # Since we don't have live schedule data, return a placeholder
        # based on the last circuit in our data
        df = self._load_race_data()
        
        # Get the most recent race data as a template
        latest = df[df['raceId'] == df['raceId'].max()].iloc[0]
        
        return {
            'name': f"{latest['country']} Grand Prix",
            'circuit': latest['name_y'],
            'location': latest['location'],
            'date': '2024 Season Data',
            'time': 'Offline Mode',
            'url': '',
            'is_placeholder': True,
        }
    
    def get_last_race(self) -> Tuple[Optional[Dict[str, Any]], Optional[List]]:
        """Get last race info and results.
        
        Returns:
            Tuple of (race_details dict, podium list) matching UI expectations
        """
        df = self._load_race_data()
        race_id = df['raceId'].max()
        
        race_df = df[df['raceId'] == race_id]
        if race_df.empty:
            return None, None
        
        race_info = race_df.iloc[0]
        
        # Race details in expected format
        race_details = {
            'name': f"{race_info['country']} Grand Prix",
            'circuit': race_info['name_y'],
            'location': race_info['location'],
            'date': '2024',
        }
        
        # Podium in expected format
        results = self.get_race_results(race_id)
        podium = []
        for result in results[:3]:
            podium.append({
                'position': str(result['position']),
                'name': result['driver_name'],
                'number': 'N/A',
                'team': result['team'],
                'code_Name': result['driver_code'],
            })
        
        return race_details, podium
    
    def get_season_info(self) -> Dict[str, Any]:
        """Get information about the data season.
        
        Returns:
            Dict with season year and data source info.
        """
        standings = self._load_standings_data()
        season = standings.get('MRData', {}).get('StandingsTable', {}).get('season', 'Unknown')
        
        return {
            'season': season,
            'data_source': 'Offline CSV/JSON',
            'last_updated': 'Static data from Ergast API archive',
        }


# Compatibility layer for existing code
class ErgastAPI(CSVDataHandler):
    """Compatibility wrapper to maintain existing API interface.
    
    Allows existing code using ErgastAPI to work with CSV data
    without major refactoring.
    """
    
    def __init__(self, cache_dir: str = None):
        """Initialize CSV handler instead of API handler."""
        # Ignore cache_dir, use project root for data files
        super().__init__()
        print("[INFO] Running in offline mode with local CSV data")
    
    def get_constructors_championship(self) -> List[Dict[str, Any]]:
        """Alias for get_constructor_standings (UI compatibility)."""
        return self.get_constructor_standings()
    
    def refresh_all_data(self) -> None:
        """No-op for offline mode. Data is static."""
        print("[INFO] Refresh skipped - running in offline mode")
        # Clear cache to reload from files if needed
        self._race_data = None
        self._standings_data = None
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Return cache status info for UI display."""
        return {
            'mode': 'offline',
            'status': 'Using local CSV data',
            'last_refresh': 'N/A (static data)',
            'api_calls_today': 0,
        }
