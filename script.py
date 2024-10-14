import requests
import json
import time
import folium
import webbrowser

# Clé API JCDecaux et ville
API_KEY = "ae7cdd5bbdb5f8b8c6204dfc290f3fff39392251"  # Remplacez par votre clé API JCDecaux
CITY = "nancy"

# URL de base pour récupérer les données des stations
URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CITY}&apiKey={API_KEY}"

# Cache pour stocker les données et gérer le rafraîchissement
cached_data = None
last_fetch_time = 0
refresh_interval = 120  # Rafraîchir les données toutes les 2 minutes (120 secondes)

# Position actuelle (remplacez par vos coordonnées si nécessaire)
my_location = [48.6937223, 6.1834097]  # Exemple : coordonnées à Nancy

# Fonction pour récupérer les données dynamiques depuis l'API JCDecaux
def fetch_dynamic_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API: {e}")
        return []

# Fonction pour gérer le cache et récupérer les données (soit du cache, soit de l'API)
def get_data():
    global cached_data, last_fetch_time

    current_time = time.time()  # Temps actuel

    # Si le cache est obsolète, on fait une nouvelle requête à l'API
    if current_time - last_fetch_time > refresh_interval:
        cached_data = fetch_dynamic_data()
        last_fetch_time = current_time
        print("Données mises à jour à partir de l'API.")
    else:
        print("Données récupérées à partir du cache.")

    return cached_data

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

        # Info-bulle pour afficher les détails de la station
        popup_info = f"{station_name}<br>Vélos disponibles : {bikes_available}<br>Bornes libres : {stands_available}"

        # Définir la couleur de l'icône selon la disponibilité des vélos
        icon_color = "green" if bikes_available > 0 else "red"

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

# Programme principal
if __name__ == "__main__":
    # Récupérer les données actualisées des stations
    stations_data = get_data()

    # Générer la carte interactive avec ces données
    if stations_data:
        generate_bike_map(stations_data)
    else:
        print("Aucune donnée disponible pour générer la carte.")

