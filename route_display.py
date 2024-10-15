from OptChemins import opt_chemins
import folium


def display_route(bike_map, stations_data):
    # Trouver les stations la plus remplie et la moins remplie
    fullest_station = None
    empty_station = None
    max_fill_percentage = -1
    min_fill_percentage = float('inf')

    for station in stations_data:
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']
        total_capacity = bikes_available + stands_available
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        if fill_percentage > max_fill_percentage:
            max_fill_percentage = fill_percentage
            fullest_station = station

        if fill_percentage < min_fill_percentage:
            min_fill_percentage = fill_percentage
            empty_station = station

    if fullest_station and empty_station:
        try:
            route_coords = opt_chemins(fullest_station['position'], empty_station['position'])
            # Afficher le chemin sur la carte
            folium.PolyLine(route_coords, color='green', weight=5, opacity=0.8).add_to(bike_map)
        except Exception as e:
            print(f"Erreur lors de l'affichage de la route : {e}")
    else:
        print("Impossible de trouver les stations les plus pleines et les plus vides.")

