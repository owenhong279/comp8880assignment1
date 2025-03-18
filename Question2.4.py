import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_degree_distribution(cities_file, edges_file):
    """
    This function is developed to answer question 2.4, and it will plot degree distribution of the network

    Parameters:
    - cities_file (str): Path to global-cities.dat file.
    - edges_file (str): Path to global-net.dat file.
    """
    # Read the nodes file (global-cities.dat) and extract node IDs
    nodes_df = pd.read_csv(cities_file, sep='|', header=None, names=['code', 'id', 'name'])
    nodes_df['id'] = nodes_df['id'].astype(int)  # Ensure node IDs are integers
    node_ids = nodes_df['id'].unique()

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
    G.add_nodes_from(node_ids)
    G.add_edges_from(edges)

    # Find the largest connected component
    largest_component = max(nx.connected_components(G), key=len)
    largest_subgraph = G.subgraph(largest_component).copy()

    # Compute degree distribution
    degree_dict = dict(largest_subgraph.degree())
    degree_values = list(degree_dict.values())
    degree_counts = {k: degree_values.count(k) for k in set(degree_values)}
    degrees, counts = zip(*sorted(degree_counts.items()))
    fractions = [c / len(largest_component) for c in counts]

    # Plot degree distribution
    plt.figure(figsize=(12, 5))

    # Standard Degree Distribution
    plt.subplot(1, 2, 1)
    plt.plot(degrees, fractions, 'bo-')
    plt.xlabel("Degree (x)")
    plt.ylabel("Fraction of Nodes (y)")
    plt.title("Degree Distribution")
    plt.grid()

    # Log-Log Degree Distribution
    plt.subplot(1, 2, 2)
    plt.loglog(degrees, fractions, 'ro-')
    plt.xlabel("log(Degree)")
    plt.ylabel("log(Fraction of Nodes)")
    plt.title("Log-Log Degree Distribution")
    plt.grid()

    plt.show()


# Result
cities_file = "data/global-cities.dat"
edges_file = "data/global-net.dat"
plot_degree_distribution(cities_file, edges_file)