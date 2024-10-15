import folium
import webbrowser
import OptChemins

# Position actuelle (remplacez par vos coordonnées si nécessaire)
my_location = [48.6937223, 6.1834097]  # Exemple : coordonnées à Nancy

# Fonction pour générer une carte interactive avec les stations de vélos
def generate_bike_map(stations_data, cyclocity_data, city_name):
    # Créer un dictionnaire avec le station_id de Cyclocity comme clé et le name comme valeur
    cyclocity_stations = {str(station['station_id']): station['name'] for station in cyclocity_data['data']['stations']}

    # Coordonnées de Nancy pour centrer la carte
    nancy_coords = [48.6937223, 6.1834097]

    # Créer la carte centrée sur Nancy
    bike_map = folium.Map(location=nancy_coords, zoom_start=14)

    # Add the optimized route as a polyline to the map
    route_coords = OptChemins.opt_chemins(stations_data[0]['position'], stations_data[1]['position'])
    folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.8).add_to(bike_map)
    nodes = OptChemins.get_all_nodes()

    for idx, node in nodes.iterrows():
        folium.CircleMarker(
            location=(node['y'], node['x']),  # Node coordinates (latitude, longitude)
            radius=2,                         # Size of the marker
            color='red',                      # Marker color
            fill=True,
            fill_opacity=0.7
        ).add_to(bike_map)


    # Ajouter un marqueur pour votre position actuelle
    folium.Marker(
        location=my_location,
        popup="Vous êtes ici",
        icon=folium.Icon(color="pink")
    ).add_to(bike_map)

    # Ajouter un marqueur pour chaque station de vélos de JCDecaux
    total_stations = len(stations_data)
    total_bikes = sum(station['available_bikes'] for station in stations_data)

    for station in stations_data:
        station_number = str(station['number'])
        station_name = cyclocity_stations.get(station_number, "Nom inconnu")

        lat = station['position']['lat']
        lon = station['position']['lng']
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']

        total_capacity = bikes_available + stands_available
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        popup_info = f"""
        <table style="white-space: nowrap; text-align: left;">
            <tr><th colspan="2" style="text-align:center;">{station_name}</th></tr>
            <tr><td>Vélos disponibles :</td><td>{bikes_available}</td></tr>
            <tr><td>Bornes libres :</td><td>{stands_available}</td></tr>
            <tr><td>Remplissage :</td><td>{int(fill_percentage)}%</td></tr>
        </table>
        """

        if fill_percentage == 100:
            icon_color = "red"
        elif fill_percentage >= 75:
            icon_color = "orange"
        elif fill_percentage >= 25:
            icon_color = "green"
        elif fill_percentage > 0:
            icon_color = "blue"
        else:
            icon_color = "darkblue"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_info, max_width=300),
            icon=folium.Icon(color=icon_color)
        ).add_to(bike_map)

    # Ajouter le titre avec la ville et les informations sur les stations
    title_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; width: 300px; height: auto;
                    background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                    padding: 10px;">
            <h4 style="margin-bottom: 5px; font-size: 20px;"><b>Ville : {city_name.capitalize()}</b></h4>
            <p>Nombre de stations : {total_stations}</p>
            <p>Nombre de vélos disponibles : {total_bikes}</p>
        </div>
    """
    bike_map.get_root().html.add_child(folium.Element(title_html))

    legend_html = """
        <div style="position: fixed;
                    bottom: 50px; left: 50px; width: 220px; height: auto;
                    background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                    padding: 10px;">
            <b>Légende des stations</b><br>
            &nbsp; <i class="fa fa-map-marker" style="color:red"></i>&nbsp; Station pleine<br>
            &nbsp; <i class="fa fa-map-marker" style="color:orange"></i>&nbsp; 75% à 99% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:green"></i>&nbsp; 25% à 75% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:blue"></i>&nbsp; 1% à 25% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:darkblue"></i>&nbsp; Station vide
        </div>
        """
    bike_map.get_root().html.add_child(folium.Element(legend_html))

    # Sauvegarder la carte dans un fichier HTML
    bike_map.save("bike_map_nancy.html")
    print(f"Carte mise à jour pour la ville de {city_name.capitalize()} sauvegardée dans 'bike_map_nancy.html'")

    # Ouvrir le fichier HTML dans le navigateur par défaut
    webbrowser.open("bike_map_nancy.html")







