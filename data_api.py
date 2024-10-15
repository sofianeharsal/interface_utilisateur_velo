import requests


# Clé API JCDecaux et ville
API_KEY = "ae7cdd5bbdb5f8b8c6204dfc290f3fff39392251"  # Remplacez par votre clé API JCDecaux
CITY = "nancy"

# URL de base pour récupérer les données des stations
JCDECAUX_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CITY}&apiKey={API_KEY}"
CYCLOCITY_URL = "https://api.cyclocity.fr/contracts/nancy/gbfs/station_information.json"

# Fonction pour récupérer les données des stations de l'API JCDecaux
def fetch_jcdecaux_data():
    try:
        response = requests.get(JCDECAUX_URL)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API JCDecaux: {e}")
        return []

# Fonction pour récupérer les données des stations de l'API Cyclocity
def fetch_cyclocity_data():
    try:
        response = requests.get(CYCLOCITY_URL)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API Cyclocity: {e}")
        return []

