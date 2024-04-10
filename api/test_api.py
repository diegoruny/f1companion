
import requests

def test_ergast_api():
    url = "http://ergast.com/api/f1/driverStandings/1.json"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        print("Conexión exitosa. Aquí hay un poco de información recibida:")
        print(data)
    else:
        print("Error al conectar con la Ergast API. Código de estado:", response.status_code)

if __name__ == "__main__":
    test_ergast_api()
