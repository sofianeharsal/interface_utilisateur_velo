from geopy.distance import geodesic


# Fonction principale pour gérer les stations et retourner la station de départ et d'arrivée
def gestion_stations(stations_data):
    start_station, end_station = end(stations_data)

    return start_station, end_station


# Fonction pour déterminer la station de départ en fonction du pourcentage de vélos disponibles
def start(stations_data):
    list_percentage = get_list_percentage(stations_data)

    # Trouver le pourcentage maximum de vélos disponibles
    max_percentage = max(list_percentage)

    # Déterminer la station de départ en fonction de ce pourcentage
    start_station = stations_data[list_percentage.index(max_percentage) + 2]

    return start_station


# Fonction pour déterminer la station d'arrivée en fonction de la distance et du pourcentage de vélos disponibles
def end(stations_data):
    list_percentage = get_list_percentage(stations_data)
    list_index_min = []  # Liste des indices des stations avec un pourcentage faible de vélos
    list_index_zero = []  # Liste des indices des stations avec 0 vélos disponibles
    last_distance = 1000000.0  # Initialiser la distance à une grande valeur
    end_station = stations_data[2]  # Station d'arrivée par défaut

    # Parcourir la liste des pourcentages pour classer les stations
    for i in range(len(list_percentage)):
        percentage = list_percentage[i]
        if percentage == 0:
            list_index_zero.append(i)  # Station avec 0 vélos disponibles
        elif 1 <= percentage < 25:
            list_index_min.append(i)  # Station avec peu de vélos disponibles

    # Obtenir la station de départ
    start_station = start(stations_data)

    # Utiliser les stations avec 0 vélos ou peu de vélos disponibles
    if list_index_zero:
        list_index = list_index_zero
    else:
        list_index = list_index_min

    # Trouver la station d'arrivée la plus proche de la station de départ
    for index in list_index:
        station = stations_data[index + 2]
        start_coord = [float(start_station['position']['lat']), float(start_station['position']['lng'])]
        end_coord = [float(station['position']['lat']), float(station['position']['lng'])]
        distance = geodesic(start_coord, end_coord).kilometers

        # Si la station est plus proche, la sélectionner comme nouvelle station d'arrivée
        if distance < last_distance:
            last_distance = distance
            end_station = station

    return start_station, end_station


# Fonction pour obtenir la liste des pourcentages de vélos disponibles dans chaque station
def get_list_percentage(stations_data):
    list_percentage = []

    # Parcourir les stations et calculer le pourcentage de vélos disponibles
    for i in range(2, len(stations_data)):
        station = stations_data[i]
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']

        # Calculer la capacité totale de la station
        total_capacity = bikes_available + stands_available

        # Calculer le pourcentage de vélos disponibles
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        list_percentage.append(fill_percentage)

    return list_percentage