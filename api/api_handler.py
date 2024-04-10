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
            "time": next_race['time'],
            "url": next_race['url'],
            "location": f"{next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}"
        }
            return race_details
        else:
            print("Failed to retrieve the next race:", response.status_code)
            return None
        
    def get_driver_standings(self):
        response = requests.get(f"{self.BASE_URL}/current/driverStandings.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            return standings
        return None

    def get_constructor_standings(self):
        response = requests.get(f"{self.BASE_URL}/current/constructorStandings.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            return standings
        return None


# if __name__ == "__main__":
#     nextRace = ErgastAPI().get_next_race()
#     print(nextRace)