
import requests

def test_ergast_api():
    url = "http://ergast.com/api/f1/current/next.json"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        print("Conexión exitosa. Aquí hay un poco de información recibida:")
        print("Raw data:\n", data)
        print("Next Race Data:\n", data['MRData']['RaceTable']['Races'][0])
        print("Some next race Data:\n, data['MRData']['RaceTable']['Races'][0]['date']")
        print("Specifically Time:\n", data['MRData']['RaceTable']['Races'][0]['time'])

    else:
        print("Error al conectar con la Ergast API. Código de estado:", response.status_code)

if __name__ == "__main__":
    test_ergast_api()
