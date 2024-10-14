# map_creator.py
import folium
import webbrowser

# Position actuelle (remplacez par vos coordonnées si nécessaire)
my_location = [48.6937223, 6.1834097]  # Exemple : coordonnées à Nancy

# Fonction pour générer une carte interactive avec les stations de vélos
def generate_bike_map(stations_data):
    # Coordonnées de Nancy pour centrer la carte
    nancy_coords = [48.6937223, 6.1834097]

    # Créer la carte centrée sur Nancy
    bike_map = folium.Map(location=nancy_coords, zoom_start=14)

    # Ajouter un marqueur pour votre position actuelle
    folium.Marker(
        location=my_location,
        popup="Vous êtes ici",
        icon=folium.Icon(color="blue")  # Couleur bleue pour l'icône de position
    ).add_to(bike_map)

    # Ajouter un marqueur pour chaque station de vélos
    for station in stations_data:
        station_name = station['name']
        lat = station['position']['lat']
        lon = station['position']['lng']
        bikes_available = station['available_bikes']
        stands_available = station['available_bike_stands']

        # Calculer la capacité totale de la station
        total_capacity = bikes_available + stands_available

        # Calculer le pourcentage de remplissage
        fill_percentage = (bikes_available / total_capacity * 100) if total_capacity > 0 else 0

        # Info-bulle pour afficher les détails de la station
        popup_info = (
            f"{station_name}<br>"
            f"Vélos disponibles : {bikes_available}<br>"
            f"Bornes libres : {stands_available}<br>"
            f"Pourcentage de remplissage : {int(fill_percentage)}%"  # Utiliser int() pour supprimer les décimales
        )

        # Définir la couleur de l'icône selon le pourcentage de remplissage
        if fill_percentage == 100:
            icon_color = "red"  # 100% de remplissage
        elif fill_percentage >= 75:
            icon_color = "orange"  # Entre 75% et 99%
        elif fill_percentage >= 25:  # Mise à jour ici pour le vert
            icon_color = "green"  # Entre 25% et 75%
        elif fill_percentage > 0:
            icon_color = "blue"  # Entre 1% et 25%
        else:
            icon_color = "darkblue"  # 0% de remplissage

        # Ajouter le marqueur à la carte
        folium.Marker(
            location=[lat, lon],
            popup=popup_info,
            icon=folium.Icon(color=icon_color)
        ).add_to(bike_map)

    # Ajouter un script JavaScript pour recharger la page toutes les 2 minutes
    bike_map.get_root().html.add_child(folium.Element("""
        <script>
            setTimeout(function() {
                location.reload();
            }, 120000); // 120000 milliseconds = 2 minutes
        </script>
    """))

    # Sauvegarder la carte dans un fichier HTML
    bike_map.save("bike_map_nancy.html")
    print("Carte mise à jour sauvegardée dans 'bike_map_nancy.html'")

    # Ouvrir le fichier HTML dans le navigateur par défaut
    webbrowser.open("bike_map_nancy.html")  # Ouvre le fichier dans le navigateur
