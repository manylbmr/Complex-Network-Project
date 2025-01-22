import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Function to simulate node percolation with debug
def node_percolation_debug(graph, p):
    nodes_to_keep = np.random.choice(graph.nodes(), size=int(p * graph.number_of_nodes()), replace=False)
    subgraph = graph.subgraph(nodes_to_keep)
    if len(subgraph) == 0:
        return 0
    largest_component = max(nx.connected_components(subgraph), key=len)
    
    return len(largest_component)

# Function to simulate node percolation
def node_percolation(graph, p):
    nodes_to_keep = np.random.choice(graph.nodes(), size=int(p * graph.number_of_nodes()), replace=False)
    subgraph = graph.subgraph(nodes_to_keep)
    if len(subgraph) == 0:
        return 0
    largest_component = max(nx.connected_components(subgraph), key=len)
    return len(largest_component)

# Function to simulate and plot percolation
def simulate_percolation(graph, p_values, num_trials, node_percolation_func):
    avg_largest_component_sizes = []
    for p in p_values:
        sizes = [node_percolation_func(graph, p) for _ in range(num_trials)]
        avg_size = np.mean(sizes)
        avg_largest_component_sizes.append(avg_size)
    return avg_largest_component_sizes

# Load the original graph

G_ref = nx.read_gexf("reseaux_complexes/football_network.gexf")

# Generate random graphs
N = G_ref.number_of_nodes()
E = G_ref.number_of_edges()
p_er = 2 * E / (N * (N - 1))
G_er = nx.erdos_renyi_graph(N, p_er)
G_conf = nx.Graph(nx.configuration_model([d for n, d in G_ref.degree()]))

# Define p values and number of trials
p_values = np.linspace(0.1, 1.0, 20)
num_trials = 30

# Simulate percolation for each graph
sizes_ref = simulate_percolation(G_ref, p_values, num_trials, node_percolation)
sizes_er = simulate_percolation(G_er, p_values, num_trials, node_percolation)
sizes_conf = simulate_percolation(G_conf, p_values, num_trials, node_percolation)

# Plot the results for the reference network
plt.figure(figsize=(10, 6))
plt.plot(p_values, sizes_ref, label="Reference Network", marker='o')
plt.plot(p_values, sizes_er, label="Erdős-Rényi Graph", marker='s')
plt.plot(p_values, sizes_conf, label="Configuration Graph", marker='^')
plt.xlabel("Occupation Probability p")
plt.ylabel("Size of the Largest Component")
plt.title("Effect of Node Percolation on the Size of the Largest Component")
plt.legend()
plt.grid(True)
plt.show()

# Use the debug function for a single run to see details
sizes_ref_debug = simulate_percolation(G_ref, p_values, num_trials, node_percolation_debug)

def degree_threshold_percolation(graph, degree_threshold):
    nodes_to_keep = [node for node, degree in graph.degree() if degree <= degree_threshold]
    subgraph = graph.subgraph(nodes_to_keep)
    if len(subgraph) == 0:
        return 0
    largest_component = max(nx.connected_components(subgraph), key=len)
    return len(largest_component)

def simulate_non_uniform_percolation(graph, degree_thresholds):
    largest_component_sizes = []
    for threshold in degree_thresholds:
        size = degree_threshold_percolation(graph, threshold)
        largest_component_sizes.append(size)
    return largest_component_sizes

# Define the degree thresholds to test
degree_thresholds = range(1, max(dict(G_ref.degree()).values()) + 1, 5)

# Simulate non-uniform percolation for each graph
sizes_ref_non_uniform = simulate_non_uniform_percolation(G_ref, degree_thresholds)
sizes_er_non_uniform = simulate_non_uniform_percolation(G_er, degree_thresholds)
sizes_conf_non_uniform = simulate_non_uniform_percolation(G_conf, degree_thresholds)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(degree_thresholds, sizes_ref_non_uniform, label="Reference Network", marker='o')
plt.plot(degree_thresholds, sizes_er_non_uniform, label="Erdős-Rényi Graph", marker='s')
plt.plot(degree_thresholds, sizes_conf_non_uniform, label="Configuration Graph", marker='^')
plt.xlabel("Degree Threshold $k_{th}$")
plt.ylabel("Size of the Largest Component")
plt.title("Effect of Non-Uniform Percolation on the Size of the Largest Component")
plt.legend()
plt.grid(True)
plt.show()
