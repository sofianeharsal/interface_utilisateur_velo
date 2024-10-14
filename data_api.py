import requests
import time

# Clé API JCDecaux et ville
API_KEY = "ae7cdd5bbdb5f8b8c6204dfc290f3fff39392251"  # Remplacez par votre clé API JCDecaux
CITY = "nancy"

# URL de base pour récupérer les données des stations
URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CITY}&apiKey={API_KEY}"

# Cache pour stocker les données et gérer le rafraîchissement
cached_data = None
last_fetch_time = 0
refresh_interval = 120  # Rafraîchir les données toutes les 2 minutes (120 secondes)

# Fonction pour récupérer les données dynamiques depuis l'API JCDecaux
def fetch_dynamic_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API: {e}")
        return []

# Fonction pour gérer le cache et récupérer les données (soit du cache, soit de l'API)
def get_data():
    global cached_data, last_fetch_time

    current_time = time.time()  # Temps actuel

    # Si le cache est obsolète, on fait une nouvelle requête à l'API
    if current_time - last_fetch_time > refresh_interval:
        cached_data = fetch_dynamic_data()
        last_fetch_time = current_time
        print("Données mises à jour à partir de l'API.")
    else:
        print("Données récupérées à partir du cache.")

    return cached_data