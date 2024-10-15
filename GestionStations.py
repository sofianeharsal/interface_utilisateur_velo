from geopy.distance import geodesic


def gestion_stations(stations_data):
    start_station, end_station = end(stations_data)

    return start_station, end_station


def start(stations_data):
    list_percentage = get_list_percentage(stations_data)

    max_percentage = max(list_percentage)

    start_station = stations_data[list_percentage.index(max_percentage) + 2]

    return start_station


def end(stations_data):
    list_percentage = get_list_percentage(stations_data)
    list_index_min = []
    list_index_zero = []
    last_distance = 1000000.0
    end_station = stations_data[2]

    for i in range(len(list_percentage)):
        percentage = list_percentage[i]
        if percentage == 0:
            list_index_zero.append(i)
        elif 1 <= percentage < 25:
            list_index_min.append(i)

    start_station = start(stations_data)

    if list_index_zero:
        list_index = list_index_zero
    else:
        list_index = list_index_min

    for index in list_index:
        station = stations_data[index + 2]
        start_coord = [float(start_station['position']['lat']), float(start_station['position']['lng'])]
        end_coord = [float(station['position']['lat']), float(station['position']['lng'])]
        distance = geodesic(start_coord, end_coord).kilometers

        if distance < last_distance:
            last_distance = distance
            end_station = station

    return start_station, end_station


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