import time
from data_api import fetch_jcdecaux_data, fetch_cyclocity_data
from map_creator import generate_bike_map

# Rafraîchissement toutes les 2 minutes (120 secondes)
refresh_interval = 120

if __name__ == "__main__":
    while True:
        # Récupérer les données actualisées des stations
        stations_data = fetch_jcdecaux_data()
        cyclocity_data = fetch_cyclocity_data()

        # Vérifier que les données sont disponibles avant de générer la carte
        if stations_data and cyclocity_data:
            print("Données mises à jour à partir des APIs.")
            generate_bike_map(stations_data, cyclocity_data)
        else:
            print("Aucune donnée disponible pour générer la carte.")

        # Attendre l'intervalle de rafraîchissement
        time.sleep(refresh_interval)

