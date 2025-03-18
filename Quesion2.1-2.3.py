import pandas as pd
import networkx as nx

def analyze_graph(cities_file, edges_file):
    """
    This function is developed to solve question 2.1, 2.2 and 2.3

    Parameters:
    - cities_file (str): Path to the global-cities.dat file.
    - edges_file (str): Path to the global-net.dat file.

    Returns:
    - num_nodes (int): Total number of unique nodes.
    - num_edges (int): Total number of undirected edges.
    - num_components (int): Number of connected components.
    - largest_component_nodes (int): Number of nodes in largest component.
    - largest_component_edges (int): Number of edges in largest component.
    - top_10_airports (list): List top 10 airports with highest degree.
    """
    # Read nodes file and get unique node IDs and airport names
    nodes_df = pd.read_csv(cities_file, sep='|', header=None, names=['code', 'id', 'name'])
    nodes_df['id'] = nodes_df['id'].astype(int)  # Ensure node IDs are integers
    node_id_to_name = dict(zip(nodes_df['id'], nodes_df['name']))
    node_ids = nodes_df['id'].unique()
    num_nodes = len(node_ids)

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

    num_edges = len(edges)

    # Create graph using NetworkX
    G = nx.Graph()
    G.add_nodes_from(node_ids)
    G.add_edges_from(edges)

    # Compute connected components
    components = list(nx.connected_components(G))
    num_components = len(components)

    # Find largest connected component
    largest_component = max(components, key=len)
    largest_component_nodes = len(largest_component)

    # Create a subgraph of largest component and count edges
    largest_subgraph = G.subgraph(largest_component).copy()
    largest_component_edges = largest_subgraph.number_of_edges()

    # Find top 10 nodes by degree in the largest component
    degree_dict = dict(largest_subgraph.degree())
    top_10_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)[:10]

    # Convert node IDs to airport names (only if exist)
    top_10_airports = [(node_id_to_name[node], degree_dict[node]) for node in top_10_nodes if node in node_id_to_name]

    return num_nodes, num_edges, num_components, largest_component_nodes, largest_component_edges, top_10_airports


# Results
cities_file = "data/global-cities.dat"
edges_file = "data/global-net.dat"
nodes, edges, components, largest_nodes, largest_edges, top_airports = analyze_graph(cities_file, edges_file)
print(f"Total nodes: {nodes}")
print(f"Total undirected edges: {edges}")
print(f"Number of connected components: {components}")
print(f"Largest component contains {largest_nodes} nodes and {largest_edges} edges")
print("Top 10 airports with highest degree:")
for airport, degree in top_airports:
    print(f"{airport}: {degree} connections")
