import pandas as pd
import networkx as nx


def compute_diameter_and_longest_path(cities_file, edges_file):
    """
    This function helps us find the longest (unweighted) shortest path between two cities and names of
    the city/airport,

    Parameters:
    - cities_file (str): Path to the global-cities.dat file.
    - edges_file (str): Path to the global-net.dat file.

    Returns:
    - diameter (int): The unweighted diameter of the largest component.
    - longest_path (list): A longest shortest path between two cities (airport names).
    """
    # Read the nodes file (global-cities.dat) and extract node IDs and airport names
    nodes_df = pd.read_csv(cities_file, sep='|', header=None, names=['code', 'id', 'name'])
    nodes_df['id'] = nodes_df['id'].astype(int)  # Ensure node IDs are integers
    node_id_to_name = dict(zip(nodes_df['id'], nodes_df['name']))

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

    # Find the largest connected component
    largest_component = max(nx.connected_components(G), key=len)
    largest_subgraph = G.subgraph(largest_component).copy()

    # Compute the diameter (longest shortest path)
    diameter = nx.diameter(largest_subgraph)

    # Compute the longest shortest path (path between two farthest nodes)
    eccentricity = nx.eccentricity(largest_subgraph)
    farthest_node = max(eccentricity, key=eccentricity.get)
    longest_path = nx.shortest_path(largest_subgraph, source=farthest_node)
    longest_path = max(longest_path.values(), key=len)

    # Convert node IDs to airport names
    longest_path_names = [node_id_to_name[node] for node in longest_path if node in node_id_to_name]

    return diameter, longest_path_names


# Example usage:
cities_file = "data/global-cities.dat"
edges_file = "data/global-net.dat"
diameter, longest_path = compute_diameter_and_longest_path(cities_file, edges_file)
print(f"Diameter of the largest component: {diameter}")
print("Longest shortest path between two cities:")
print(" -> ".join(longest_path))