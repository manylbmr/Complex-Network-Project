import networkx as nx
import community as community_louvain  # For the Louvain algorithm
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import louvain_communities

# Load the original graph

G_ref = nx.read_gexf("reseaux_complexes/football_network.gexf")

# Get the parameters of the original graph
N = G_ref.number_of_nodes()
E = G_ref.number_of_edges()
degree_sequence = [d for n, d in G_ref.degree()]

# Calculate the probability p for the Erdős-Rényi model
p = 2 * E / (N * (N - 1))

# Generate an Erdős-Rényi graph
G_er = nx.erdos_renyi_graph(N, p)

# Generate a Configuration graph
G_conf = nx.Graph(nx.configuration_model(degree_sequence))

# Function to detect and visualize communities
def detect_and_visualize_communities(G, title):
    # Apply the Louvain algorithm
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    
    # Distribution of community sizes
    community_sizes = np.bincount(list(partition.values()))

    # Get positions for visualization
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes based on communities
    communities = louvain_communities(G)
    community_colors = {node: i for i, community in enumerate(communities) for node in community}
    node_colors = [community_colors[node] for node in G.nodes()]

    plt.figure(figsize=(12, 12))
    nodes = nx.draw_networkx_nodes(G, pos, node_size=30, node_color=node_colors, cmap=plt.cm.rainbow, alpha=0.7)
   
    plt.title(f"{title}\nModularité: {modularity:.4f}")
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()

    # Display the distribution of community sizes
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(community_sizes)), community_sizes, color='skyblue')
    plt.title(f"Distribution of Community Sizes - {title}")
    plt.xlabel("Communities")
    plt.ylabel("Number of Nodes")
    plt.show()

# Visualize communities for the reference graph
detect_and_visualize_communities(G_ref, "Communities in the Reference Network")

# Visualize communities for the Erdős-Rényi graph
detect_and_visualize_communities(G_er, "Communities in the Erdős-Rényi Graph")

# Visualize communities for the Configuration graph
detect_and_visualize_communities(G_conf, "Communities in the Configuration Graph")
