import networkx as nx

# Load the original graph
G = nx.read_gexf("reseaux_complexes/football_network.gexf")

# Step 1: Get the parameters of the original graph
N = G.number_of_nodes()

E = G.number_of_edges()
degree_sequence = [d for n, d in G.degree()]

# Calculate the probability p for Erdős-Rényi
p = 2 * E / (N * (N - 1))
print("p=", p)  

# Step 2: Generate 3 Erdős-Rényi graphs
erdos_renyi_graphs = [nx.erdos_renyi_graph(N, p) for _ in range(3)]

# Step 3: Generate 8 graphs according to the Configuration model
configuration_graphs = [nx.configuration_model(degree_sequence) for _ in range(8)]

# Convert MultiGraphs to simple Graphs (removing loops and multiple edges)
configuration_graphs = [nx.Graph(graph) for graph in configuration_graphs]

# Function to display graph information
def print_graph_info(graphs, title_prefix):
    for i, graph in enumerate(graphs):
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        degree_sequence = [d for n, d in graph.degree()]
        average_degree = sum(degree_sequence) / num_nodes
        print(f"{title_prefix} Graph {i + 1}:")
        print(f"  Number of nodes : {num_nodes}")
        print(f"  Number of edges : {num_edges}")
        print(f"  Mean Degree : {average_degree:.2f}")
        print(f"  Degree distribution : {degree_sequence[:10]}...")  # Display the first 10 degrees for an overview
        print()

# Display information of Erdős-Rényi graphs
print_graph_info(erdos_renyi_graphs, "Erdős-Rényi")

# Display information of Configuration graphs
print_graph_info(configuration_graphs, "Configuration")
