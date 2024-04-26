# Version: 1.0
import requests

class ErgastAPI:
    BASE_URL = "http://ergast.com/api/f1"

    def get_next_race(self):
        response = requests.get(f"{self.BASE_URL}/current/next.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            next_race = data['MRData']['RaceTable']['Races'][0]
            # Extraer y retornar solo los datos relevantes
            race_details = {
            "name": next_race['raceName'],
            "circuit": next_race['Circuit']['circuitName'],
            "date": next_race['date'],
            "time": next_race['time'], #Is not returning the time to the card
            "url": next_race['url'],
            "location": f"{next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}"
        }
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


            
        
    def get_driver_standings(self):
        response = requests.get(f"{self.BASE_URL}/current/driverStandings.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            standings = sorted(standings, key=lambda x: int(x['position']))
            return standings
        return None

    def get_constructor_standings(self):
        response = requests.get(f"{self.BASE_URL}/current/constructorStandings.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            return standings
        return None

