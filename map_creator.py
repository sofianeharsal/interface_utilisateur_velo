import folium
import webbrowser

# Position actuelle (remplacez par vos coordonnées si nécessaire)
my_location = [48.6937223, 6.1834097]  # Exemple : coordonnées à Nancy

# Fonction pour générer une carte interactive avec les stations de vélos
def generate_bike_map(stations_data, cyclocity_data):
    # Créer un dictionnaire avec le station_id de Cyclocity comme clé et le name comme valeur
    cyclocity_stations = {str(station['station_id']): station['name'] for station in cyclocity_data['data']['stations']}

    # Coordonnées de Nancy pour centrer la carte
    nancy_coords = [48.6937223, 6.1834097]

    # Créer la carte centrée sur Nancy
    bike_map = folium.Map(location=nancy_coords, zoom_start=14)

    # Ajouter un marqueur pour votre position actuelle
    folium.Marker(
        location=my_location,
        popup="Vous êtes ici",
        icon=folium.Icon(color="pink")  # Couleur bleue pour l'icône de position
    ).add_to(bike_map)

    # Variables pour compter le nombre total de vélos et de stations
    total_bikes = 0
    total_stations = len(stations_data)  # On définit total_stations ici

    # Ajouter un marqueur pour chaque station de vélos de JCDecaux
    for station in stations_data:
        station_number = str(station['number'])  # Convertir 'number' de JCDecaux en chaîne pour correspondance
        station_name = cyclocity_stations.get(station_number, "Nom inconnu")  # Utiliser le nom de Cyclocity ou "Nom inconnu" si non trouvé

        lat = station['position']['lat']
        lon = station['position']['lng']
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']

        # Ajouter au total de vélos disponibles
        total_bikes += bikes_available

        # Calculer la capacité totale de la station
        total_capacity = bikes_available + stands_available

        # Calculer le pourcentage de remplissage
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        # Info-bulle formatée en tableau HTML pour un meilleur alignement
        popup_info = f"""
        <table style="white-space: nowrap; text-align: left;">
            <tr><th colspan="2" style="text-align:center;">{station_name}</th></tr>
            <tr><td>Vélos disponibles :</td><td>{bikes_available}</td></tr>
            <tr><td>Bornes libres :</td><td>{stands_available}</td></tr>
            <tr><td>Remplissage :</td><td>{int(fill_percentage)}%</td></tr>
        </table>
        """

        # Définir la couleur de l'icône selon le pourcentage de remplissage
        if fill_percentage == 100:
            icon_color = "red"  # 100% de remplissage
        elif fill_percentage >= 75:
            icon_color = "orange"  # Entre 75% et 99%
        elif fill_percentage >= 25:
            icon_color = "green"  # Entre 25% et 75%
        elif fill_percentage > 0:
            icon_color = "blue"  # Entre 1% et 25%
        else:
            icon_color = "darkblue"  # 0% de remplissage

        # Ajouter le marqueur à la carte avec l'info-bulle alignée
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_info, max_width=300),
            icon=folium.Icon(color=icon_color)
        ).add_to(bike_map)

    # Ajouter un script HTML pour la légende des couleurs des stations
    legend_html = """
        <div style="position: fixed;
                    bottom: 50px; left: 50px; width: 220px; height: auto;
                    background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                    padding: 10px;">
            <b>Légende des stations</b><br>
            &nbsp; <i class="fa fa-map-marker" style="color:red"></i>&nbsp; 100% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:orange"></i>&nbsp; 75% - 99% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:green"></i>&nbsp; 25% - 75% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:blue"></i>&nbsp; 1% - 25% de remplissage<br>
            &nbsp; <i class="fa fa-map-marker" style="color:darkblue"></i>&nbsp; 0% de remplissage
        </div>
        """
    bike_map.get_root().html.add_child(folium.Element(legend_html))

    # Ajouter un encadré de titre en haut à gauche avec le nom de la ville, le nombre de stations et le nombre de vélos disponibles
    title_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; width: 300px; height: auto;
                    background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                    padding: 10px;">
            <h4 style="margin-bottom: 5px; font-size: 20px;"><b>Nancy</b></h4>  <!-- Taille de police augmentée à 20px -->
            <p>Nombre de stations : {total_stations}</p>
            <p>Nombre de vélos disponibles : {total_bikes}</p>
        </div>
    """
    bike_map.get_root().html.add_child(folium.Element(title_html))

    # Sauvegarder la carte dans un fichier HTML
    bike_map.save("bike_map_nancy.html")
    print("Carte mise à jour sauvegardée dans 'bike_map_nancy.html'")

    # Ouvrir le fichier HTML dans le navigateur par défaut
    webbrowser.open("bike_map_nancy.html")  # Ouvre le fichier dans le navigateur






