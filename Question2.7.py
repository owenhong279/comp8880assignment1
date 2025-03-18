import pandas as pd
import networkx as nx


def find_top_central_airports(cities_file, edges_file, top_n=10):
    """
    This function find top N most central airports in the largest component based on betweenness centrality.

    Parameters:
    - cities_file (str): Path to the global-cities.dat file.
    - edges_file (str): Path to the global-net.dat file.
    - top_n (int): Number of top airports to return.

    Returns:
    - top_central_airports (list): List of tuples (airport name, betweenness centrality value).
    """
    # Read the nodes file (global-cities.dat) and extract node IDs and airport names
    nodes_df = pd.read_csv(cities_file, sep='|', header=None, names=['code', 'id', 'name'])
    nodes_df['id'] = nodes_df['id'].astype(int)  # Ensure node IDs are integers
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

    # Find the largest connected component
    largest_component = max(nx.connected_components(G), key=len)
    largest_subgraph = G.subgraph(largest_component).copy()

    # Compute betweenness centrality
    betweenness = nx.betweenness_centrality(largest_subgraph)

    # Get the top N airports by betweenness centrality
    top_nodes = sorted(betweenness, key=betweenness.get, reverse=True)[:top_n]

    # Convert node IDs to airport names
    top_central_airports = [(id_to_name[node], betweenness[node]) for node in top_nodes if node in id_to_name]

    return top_central_airports


# Result
cities_file = "data/global-cities.dat"
edges_file = "data/global-net.dat"
top_airports = find_top_central_airports(cities_file, edges_file, top_n=10)

print("Top 10 most central airports by betweenness:")
for airport, centrality in top_airports:
    print(f"{airport}: {centrality:.5f}")
