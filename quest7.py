import networkx as nx
import numpy as np

# Load the reference graph
G_ref = nx.read_gexf("reseaux_complexes/football_network.gexf")

# Get the parameters of the reference graph
N = G_ref.number_of_nodes()
E = G_ref.number_of_edges()
degree_sequence = [d for n, d in G_ref.degree()]

# Calculate the probability p for the Erdős-Rényi model

p = 2 * E / (N * (N - 1))

# Function to calculate metrics for a given graph
def calculate_metrics(graph):
    try:
        # Degree centrality
        degree_centrality = nx.degree_centrality(graph)
        avg_degree_centrality = np.mean(list(degree_centrality.values()))
        
        # Eigenvector centrality with iteration limit
        eigenvector_centrality = nx.eigenvector_centrality(graph, max_iter=100, tol=1e-06)
        avg_eigenvector_centrality = np.mean(list(eigenvector_centrality.values()))
        
        # Approximate betweenness centrality
        betweenness_centrality = nx.betweenness_centrality(graph, k=10, seed=42)  # Approximation with k nodes
        avg_betweenness_centrality = np.mean(list(betweenness_centrality.values()))
        
        # Clustering coefficient
        clustering_coefficients = nx.clustering(graph)
        avg_clustering_coefficient = np.mean(list(clustering_coefficients.values()))
        
        # Distribution of nodes in components
        components = list(nx.connected_components(graph))
        largest_component_size = len(max(components, key=len))
        other_components_size = sum(len(comp) for comp in components) - largest_component_size
        
        return {
            "avg_degree_centrality": avg_degree_centrality,
            "avg_eigenvector_centrality": avg_eigenvector_centrality,
            "avg_betweenness_centrality": avg_betweenness_centrality,
            "avg_clustering_coefficient": avg_clustering_coefficient,
            "largest_component_size": largest_component_size,
            "other_components_size": other_components_size,
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None

# Calculate metrics for the reference network
metrics_ref = calculate_metrics(G_ref)

# Generate and calculate metrics for random graphs
erdos_renyi_graphs = [nx.erdos_renyi_graph(N, p) for _ in range(3)]
configuration_graphs = [nx.Graph(nx.configuration_model(degree_sequence)) for _ in range(8)]

# Calculate metrics for Erdős-Rényi graphs
metrics_er = [calculate_metrics(graph) for graph in erdos_renyi_graphs if graph]

# Calculate metrics for Configuration graphs
metrics_conf = [calculate_metrics(graph) for graph in configuration_graphs if graph]

# Function to display results for each graph
def display_metrics_for_each_graph(metrics_list, title_prefix):
    for i, metrics in enumerate(metrics_list):
        if metrics:
            print(f"\n{title_prefix} Graph {i + 1}:")
            for key, value in metrics.items():
                print(f"  {key}: {value:.4f}")
        else:
            print(f"\n{title_prefix} Graph {i + 1}: Error calculating metrics.")

# Display statistics for each Erdős-Rényi graph
display_metrics_for_each_graph(metrics_er, "Erdős-Rényi")

# Display statistics for each Configuration graph
display_metrics_for_each_graph(metrics_conf, "Configuration")

# Function to display average metrics comparison
def display_metrics_comparison(metrics_ref, metrics_random, title):
    if not metrics_ref or not metrics_random:
        print(f"Metrics for {title} could not be calculated correctly.")
        return
    
    print(f"\n{title}")
    print("Reference network:")
    for key, value in metrics_ref.items():
        print(f"  {key}: {value:.4f}")
    
    print("Average of random networks:")
    avg_metrics_random = {key: np.mean([m[key] for m in metrics_random if m]) for key in metrics_random[0]}
    for key, value in avg_metrics_random.items():
        print(f"  {key}: {value:.4f}")

# Display metrics comparison
display_metrics_comparison(metrics_ref, metrics_er, "Comparison with Erdős-Rényi graphs")
display_metrics_comparison(metrics_ref, metrics_conf, "Comparison with Configuration graphs")
