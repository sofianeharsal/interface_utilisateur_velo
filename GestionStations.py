def gestion_stations(stations_data):
    start_station = start(stations_data)
    end_station = end(stations_data)

    return start_station, end_station


def start(stations_data):
    list_percentage = get_list_percentage(stations_data)

    max_percentage = max(list_percentage)

    start_station = stations_data[list_percentage.index(max_percentage) + 2]

    return start_station


def end(stations_data):
    list_percentage = get_list_percentage(stations_data)

    min_percentage = min(list_percentage)

    end_station = stations_data[list_percentage.index(min_percentage) + 2]

    return end_station


def get_list_percentage(stations_data):
    list_percentage = []

    for i in range(2, len(stations_data)):
        station = stations_data[i]
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']

        # Calculer la capacité totale de la station
        total_capacity = bikes_available + stands_available

        # Calculer le pourcentage de remplissage
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        list_percentage.append(fill_percentage)

    return list_percentage