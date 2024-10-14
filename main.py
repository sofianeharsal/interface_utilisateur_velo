# main.py
from data_api import get_data
from map_creator import generate_bike_map

# Programme principal
if __name__ == "__main__":
    # Récupérer les données actualisées des stations
    stations_data = get_data()

    # Générer la carte interactive avec ces données
    if stations_data:
        generate_bike_map(stations_data)
    else:
        print("Aucune donnée disponible pour générer la carte.")
