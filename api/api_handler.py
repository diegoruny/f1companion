# Version: 0.01
import requests
import json
import os
import time

class ErgastAPI:
    BASE_URL = "http://ergast.com/api/f1"
    
    def get_next_race(self):
        response = requests.get(f"{self.BASE_URL}/current/next.json", timeout=5)
        print(response)
        if response.status_code == 200:
            data = response.json()
            next_race = data['MRData']['RaceTable']['Races'][0]
            print(next_race["time"])
            # Extraer y retornar solo los datos relevantes
            race_details = {
            "name": next_race['raceName'],
            "circuit": next_race['Circuit']['circuitName'],
            "date": next_race['date'],
            "time": next_race['time'],
            "url": next_race['url'],
            "location": f"{next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}"
        }
            print("holiwi",race_details)
            return race_details
        else:
            print("Failed to retrieve the next race:", response.status_code)
            return None

    def get_last_race(self):
        response = requests.get(f"{self.BASE_URL}/current/last/results.json", timeout=5)
        if response.status_code == 200:
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
                    "name": result['Driver']['givenName']+ " " + result['Driver']['familyName'],
                    "number": result['Driver']['permanentNumber'],
                    "team": result['Constructor']['name'],
                    "code_Name": result['Driver']['code'],
                }
                podium.append(driver_card)
            return race_details, podium
        else:
            print("Failed to retrieve the last race:", response.status_code)
            return None, None


            
        
    def get_driver_standings(self, CACHE_PATH='current_drivers_standings.json', cache_timeout=3600):
        data = None
        # Check if cache file exists and is not too old
        if os.path.exists(CACHE_PATH):
            file_mod_time = os.path.getmtime(CACHE_PATH)
            current_time = time.time()
            if (current_time - file_mod_time) < cache_timeout:
                with open(CACHE_PATH, 'r') as file:
                    data = json.load(file)
        
        if not data:
            response = requests.get(f"{self.BASE_URL}/current/driverStandings.json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                #Cache Data
                with open(CACHE_PATH, 'w') as file:
                    json.dump(data, file)        
        if data:
            processed_data = self.processed_standings(data)
            if processed_data:
                print("Data processed successfully")
                return processed_data
            else:
                print("Processing returned no data")
        else:
            print("No data available to process")

    def processed_standings(self, data):
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
        # print(processed_standings)
        return processed_standings
    

    def get_constructor_standings(self):
        response = requests.get(f"{self.BASE_URL}/current/constructorStandings.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            return standings
        return None

