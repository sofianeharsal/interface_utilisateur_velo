import networkx as nx
import osmnx as ox
from geopy.distance import geodesic

'''
# Fonction pour compléter la carte
def complete_map():
    # Obtenir le graphe de la ville de Nancy, France
    map_nancy = ox.graph_from_place('Nancy, France', network_type='drive')
    map_vandoeuvre = ox.graph_from_place('Vandoeuvre-lès-Nancy, France', network_type='drive')
    map_malzeville = ox.graph_from_place('Malzéville, France', network_type='drive')
    map_saintmax = ox.graph_from_place('Saint-Max, France', network_type='drive')

    # Vérifier si le système de coordonnées (CRS) est défini pour chaque graphe
    if 'crs' not in map_nancy.graph:
        map_nancy.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_vandoeuvre.graph:
        map_vandoeuvre.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_malzeville.graph:
        map_malzeville.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_saintmax.graph:
        map_saintmax.graph['crs'] = 'EPSG:4326'

    # Combiner les quatre graphes en un seul
    map_combined = nx.MultiDiGraph()

    # Ajouter la carte de Nancy au graphe combiné
    for node, data in map_nancy.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_nancy.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Ajouter la carte de Vandoeuvre-lès-Nancy au graphe combiné
    for node, data in map_vandoeuvre.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_vandoeuvre.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Ajouter la carte de Malzéville au graphe combiné
    for node, data in map_malzeville.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_malzeville.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Ajouter la carte de Saint-Max au graphe combiné
    for node, data in map_saintmax.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_saintmax.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Définir le CRS pour le graphe combiné s'il manque
    if 'crs' not in map_combined.graph:
        map_combined.graph['crs'] = 'EPSG:4326'

    return map_combined
'''


# Fonction pour optimiser les chemins entre deux points
def opt_chemins(station_deb, station_fin):
    try:
        # Récupérer les cartes combinées de Nancy, Vandoeuvre-lès-Nancy, Malzéville et Saint-Max
        # map_combined = complete_map()

        # Récupérer la carte de Nancy
        map_nancy = ox.graph_from_place('Nancy, France', network_type='drive')

        # Stocker les coordonnées de départ et d'arrivée sous forme de listes de flottants
        start_coord = [float(station_deb['lat']), float(station_deb['lng'])]
        end_coord = [float(station_fin['lat']), float(station_fin['lng'])]

        # Trouver le chemin le plus court entre deux points, minimisant le temps de trajet
        source = ox.nearest_nodes(map_nancy, float(station_deb['lng']),
                                  float(station_deb['lat']))  # Coordonnées du point de départ
        target = ox.nearest_nodes(map_nancy, float(station_fin['lng']),
                                  float(station_fin['lat']))  # Coordonnées du point d'arrivée

        # Ajouter les coordonnées de départ et d'arrivée en tant que nouveaux nœuds
        map_nancy.add_node("start", y=start_coord[0], x=start_coord[1])
        map_nancy.add_node("end", y=end_coord[0], x=end_coord[1])

        # Connecter le nouveau nœud de départ au nœud le plus proche du graphe
        start_edge_weight = calculate_edge_weight(start_coord,
                                                  (map_nancy.nodes[source]['y'], map_nancy.nodes[source]['x']))
        map_nancy.add_edge("start", source, weight=start_edge_weight)
        map_nancy.add_edge(source, "start", weight=start_edge_weight)  # Bidirectionnel

        # Connecter le nouveau nœud d'arrivée au nœud le plus proche du graphe
        end_edge_weight = calculate_edge_weight(end_coord, (map_nancy.nodes[source]['y'], map_nancy.nodes[source]['x']))
        map_nancy.add_edge("end", target, weight=end_edge_weight)
        map_nancy.add_edge(target, "end", weight=end_edge_weight)  # Bidirectionnel

        # Calculer le chemin le plus court entre le nœud de départ et celui d'arrivée
        shortest_path = nx.shortest_path(map_nancy, source="start", target="end", weight='weight')

        # Obtenir les coordonnées géographiques des nœuds le long de la route la plus courte
        route_coords = [(map_nancy.nodes[node]['y'], map_nancy.nodes[node]['x']) for node in shortest_path]

        return route_coords
    except:
        print("opt_chemins(): Une erreur est survenue.")
        return None


# Fonction pour calculer le poids des arêtes basé sur la distance géographique
def calculate_edge_weight(coord1, coord2):
    try:
        return geodesic(coord1, coord2).meters
    except:
        print("calculate_edge_weight(): Une erreur est survenue.")
        return None


'''
# Fonction pour récupérer tous les nœuds de la carte combinée
def get_all_nodes():
    nodes, edges = ox.graph_to_gdfs(complete_map(), nodes=True)
    return nodes
'''


# Fonction pour récupérer tous les nœuds de la carte de Nancy
def get_all_nodes_nancy():
    nodes, edges = ox.graph_to_gdfs(ox.graph_from_place('Nancy, France', network_type='drive'), nodes=True)
    return nodes


# Fonction pour récupérer tous les nœuds de la carte de Vandoeuvre-lès-Nancy
def get_all_nodes_vandoeuvre():
    nodes, edges = ox.graph_to_gdfs(ox.graph_from_place('Vandoeuvre-lès-Nancy, France', network_type='drive'),
                                    nodes=True)
    return nodes


# Fonction pour récupérer tous les nœuds de la carte de Malzéville
def get_all_nodes_malzeville():
    nodes, edges = ox.graph_to_gdfs(ox.graph_from_place('Malzéville, France', network_type='drive'), nodes=True)
    return nodes


# Fonction pour récupérer tous les nœuds de la carte de Saint-Max
def get_all_nodes_saintmax():
    nodes, edges = ox.graph_to_gdfs(ox.graph_from_place('Saint-Max, France', network_type='drive'), nodes=True)
    return nodes
