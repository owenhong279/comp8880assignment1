import pandas as pd
import networkx as nx


def find_shortest_flight_path(cities_file, edges_file, source_code, target_code):
    """
    This function finds the shortest path between CBR and CPT

    Parameters:
    - cities_file (str): Path to global-cities.dat file.
    - edges_file (str): Path to global-net.dat file.
    - source_code (str): Code of departure airport.
    - target_code (str): Code of destination airport.

    Returns:
    - shortest_path_length (int): Minimum number of flights required.
    - shortest_path (list): List of airport names representing the route.
    """
    # Read the nodes file (global-cities.dat) and extract node IDs and airport names
    nodes_df = pd.read_csv(cities_file, sep='|', header=None, names=['code', 'id', 'name'])
    nodes_df['id'] = nodes_df['id'].astype(int)  # Ensure node IDs are integers

    # Create mappings for code-to-ID and ID-to-name
    code_to_id = dict(zip(nodes_df['code'], nodes_df['id']))
    id_to_name = dict(zip(nodes_df['id'], nodes_df['name']))

    # Read the edges file (global-net.dat) and extract node pairs
    edges_df = pd.read_csv(edges_file, sep=r'\s+', header=None)
    edges_df[0] = edges_df[0].astype(int)  # Ensure node IDs are integers
    edges_df[1] = edges_df[1].astype(int)
    edges = set()

    # Loop through each edge and store as an undirected edge
    for _, row in edges_df.iterrows():
        node_a, node_b = row[0], row[1]
        edge = tuple(sorted([node_a, node_b]))  # Sort to ensure undirected nature
        edges.add(edge)

    # Create graph using NetworkX
    G = nx.Graph()
    G.add_edges_from(edges)

    # Get node IDs for the given IATA codes
    if source_code not in code_to_id or target_code not in code_to_id:
        return None, None  # If either airport code is missing, return None

    source_id = code_to_id[source_code]
    target_id = code_to_id[target_code]

    # Compute shortest path using BFS
    shortest_path_ids = nx.shortest_path(G, source=source_id, target=target_id)
    shortest_path_length = len(shortest_path_ids) - 1  # Number of flights

    # Convert node IDs to airport names
    shortest_path = [id_to_name[node] for node in shortest_path_ids if node in id_to_name]

    return shortest_path_length, shortest_path


# REsults
cities_file = "data/global-cities.dat"
edges_file = "data/global-net.dat"
source_airport = "CBR"  # Canberra
target_airport = "CPT"  # Cape Town

shortest_flights, route = find_shortest_flight_path(cities_file, edges_file, source_airport, target_airport)
print(f"Smallest number of flights required: {shortest_flights}")
print("Route:")
print(" <-> ".join(route))