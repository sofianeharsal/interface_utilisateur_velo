from data_api import fetch_jcdecaux_data, fetch_cyclocity_data, CITY
from map_creator import generate_bike_map

# Programme principal
if __name__ == "__main__":
    # Récupérer les données actualisées des stations
    stations_data = fetch_jcdecaux_data()
    cyclocity_data = fetch_cyclocity_data()

    # Générer la carte interactive avec ces données
    if stations_data:
        generate_bike_map(stations_data, cyclocity_data, CITY)
    else:
        print("Aucune donnée disponible pour générer la carte.")