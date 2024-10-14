import requests

# Clé API JCDecaux
API_KEY = "ae7cdd5bbdb5f8b8c6204dfc290f3fff39392251"
CITY = "nancy"

# URL pour récupérer les données des stations
URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CITY}&apiKey={API_KEY}"

# Effectuer une requête GET pour obtenir les données
response = requests.get(URL)

# Vérifier si la requête est réussie (code de statut HTTP 200)
if response.status_code == 200:
    stations_data = response.json()  # Convertir la réponse en format JSON
else:
    print("Erreur lors de la récupération des données:", response.status_code)
    stations_data = []


# Afficher les informations sur les vélos disponibles et les bornes libres pour chaque station
for station in stations_data:
    station_name = station['name']
    bikes_available = station['available_bikes']  # Vélos disponibles
    stands_available = station['available_bike_stands']  # Bornes libres
    total_stands = station['bike_stands']  # Nombre total de bornes

    print(f"Station: {station_name}")
    print(f"Vélos disponibles: {bikes_available}")
    print(f"Bornes libres: {stands_available}")
    print(f"Capacité totale: {total_stands}")
    print("-" * 30)