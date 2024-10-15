import networkx as nx
import osmnx as ox
from geopy.distance import geodesic


def complete_map():
    # Get the graph for the city of Nancy, France
    map_nancy = ox.graph_from_place('Nancy, France', network_type='drive')
    map_vandoeuvre = ox.graph_from_place('Vandoeuvre-lès-Nancy, France', network_type='drive')
    map_malzeville = ox.graph_from_place('Malzéville, France', network_type='drive')
    map_saintmax = ox.graph_from_place('Saint-Max, France', network_type='drive')

    # Check if the CRS is set for each graph
    if 'crs' not in map_nancy.graph:
        map_nancy.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_vandoeuvre.graph:
        map_vandoeuvre.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_malzeville.graph:
        map_malzeville.graph['crs'] = 'EPSG:4326'
    if 'crs' not in map_saintmax.graph:
        map_saintmax.graph['crs'] = 'EPSG:4326'

    # Combine all three graphs
    map_combined = nx.MultiDiGraph()

    # Adding the map of Nancy to the combined map
    for node, data in map_nancy.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_nancy.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Adding the map of Vandoeuvre-lès-Nancy to the combined map
    for node, data in map_vandoeuvre.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_vandoeuvre.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Adding the map of Malzéville to the combined map
    for node, data in map_malzeville.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_malzeville.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Adding the map of Saint-Max to the combined map
    for node, data in map_saintmax.nodes(data=True):
        map_combined.add_node(node, **data)

    for u, v, key, data in map_saintmax.edges(keys=True, data=True):
        map_combined.add_edge(u, v, key, **data)

    # Set the CRS for the combined graph if it's missing
    if 'crs' not in map_combined.graph:
        map_combined.graph['crs'] = 'EPSG:4326'

    return map_combined


def opt_chemins(station_deb, station_fin):
    # Fetching the combined nodes maps of Nancy, Vandoeuvre-lès-Nancy, Malzéville and Saint-Max
    map_combined = complete_map()

    # Storing the starting and ending points coordinates as lists of floats
    start_coord = [float(station_deb['lat']), float(station_deb['lng'])]
    end_coord = [float(station_fin['lat']), float(station_fin['lng'])]

    # Find the shortest path between two points, minimizing travel time
    source = ox.nearest_nodes(map_combined, float(station_deb['lng']),
                              float(station_deb['lat']))  # Coordinates of starting point
    target = ox.nearest_nodes(map_combined, float(station_fin['lng']),
                              float(station_fin['lat']))  # Coordinates of ending point

    # Add start and end coordinates as new nodes
    map_combined.add_node("start", y=start_coord[0], x=start_coord[1])
    map_combined.add_node("end", y=end_coord[0], x=end_coord[1])

    # Connect the new start node to the nearest node in the graph
    start_edge_weight = calculate_edge_weight(start_coord,
                                              (map_combined.nodes[source]['y'], map_combined.nodes[source]['x']))
    map_combined.add_edge("start", source, weight=start_edge_weight)
    map_combined.add_edge(source, "start", weight=start_edge_weight)  # Make it bidirectional

    # Connect the new end node to the nearest node in the graph
    end_edge_weight = calculate_edge_weight(end_coord,
                                            (map_combined.nodes[source]['y'], map_combined.nodes[source]['x']))
    map_combined.add_edge("end", target, weight=end_edge_weight)
    map_combined.add_edge(target, "end", weight=end_edge_weight)  # Make it bidirectional

    shortest_path = nx.shortest_path(map_combined, source="start", target="end", weight='weight')

    # Get the geographical coordinates of the nodes along the shortest route
    route_coords = [(map_combined.nodes[node]['y'], map_combined.nodes[node]['x']) for node in shortest_path]

    return route_coords


# Function to calculate edge weight based on geographic distance
def calculate_edge_weight(coord1, coord2):
    return geodesic(coord1, coord2).meters


def get_all_nodes():
    nodes, edges = ox.graph_to_gdfs(complete_map(), nodes=True)
    return nodes
