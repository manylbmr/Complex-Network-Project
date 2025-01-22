import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
file_path = 'C:/Users/bouma/intelligencia Comp/Travail 1/reseaux_complexes/appearances_reduced.csv'  
df = pd.read_csv(file_path)

# Check that the necessary columns exist
required_columns = {'game_id', 'player_id', 'player_name', 'player_club'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Your file must contain the columns {required_columns}")

# Initialize the graph
G = nx.Graph()

# Group by club
for club, club_group in df.groupby('player_club'):
    # Group by match
    for game_id, game_group in club_group.groupby('game_id'):
        players = game_group[['player_id', 'player_name']].values.tolist()  # List of (id, name) for a club and a match
        # Add edges between all pairs of players of this club and this match
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                player1_id, player1_name = players[i]
                player2_id, player2_name = players[j]
                if G.has_edge(player1_id, player2_id):
                    G[player1_id][player2_id]['weight'] += 1
                else:
                    G.add_edge(player1_id, player2_id, weight=1)
                # Add node attributes for player names
                G.nodes[player1_id]['name'] = player1_name
                G.nodes[player2_id]['name'] = player2_name
                

print(f"Graph size (number of nodes): {G.number_of_nodes()}")
print(f"Number of edges in the graph: {G.number_of_edges()}")

# 1. Player Centrality
degree_centrality = nx.degree_centrality(G)
top_5_players = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
top_5_info = [(G.nodes[player_id]['name'], round(centrality, 5)) for player_id, centrality in top_5_players]
print("Top 5 most central players:")
for name, centrality in top_5_info:
    print(f"- {name}: centrality = {centrality}")
   
print("\n") 

# 2. Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
top_5_players_eigen = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
top_5_info_eigen = [(G.nodes[player_id]['name'], round(centrality, 5)) for player_id, centrality in top_5_players_eigen]
print("Top 5 most central players:")
for name, centrality in top_5_info_eigen:
    print(f"- {name}: centrality = {centrality}")

print("\n")

# 3. Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
top_5_players_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
top_5_info_betweenness = [(G.nodes[player_id]['name'], round(centrality, 5)) for player_id, centrality in top_5_players_betweenness]
print("Top 5 most central players:")
for name, centrality in top_5_info_betweenness:
    print(f"- {name}: centrality = {centrality}")

# 2. Team Cohesion
largest_cc = max(nx.connected_components(G), key=len)
giant_component = G.subgraph(largest_cc)
print(f"Number of nodes in the largest connected component (team cohesion): {giant_component.number_of_nodes()}")

# 3. Match Participation Patterns
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
plt.figure(figsize=(10, 6))
plt.hist(edge_weights, bins=range(1, max(edge_weights) + 2), color='skyblue', edgecolor='black', align='left')
plt.title("Weight distribution by edge")
plt.xlabel("Games played together")
plt.ylabel("Pair of players")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Calculate the diameter of the network
diameter = nx.diameter(G)
print(f"Graph diameter: {diameter}")

# 4. Average Degree and Network Density
average_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
density = nx.density(G)
print(f"Average degree of the graph: {average_degree:.5f}")
print(f"Graph density: {density:.5f}")


# Load additional CSV files
player_valuations = pd.read_csv('reseaux_complexes/player_valuations.csv')
players_info = pd.read_csv('reseaux_complexes/players.csv')
game_events = pd.read_csv('reseaux_complexes/game_events.csv')
game_lineups = pd.read_csv('reseaux_complexes/game_lineups.csv')

# Add nationality to nodes
for node in G.nodes():
    G.nodes[node]['nationality'] = players_info.loc[players_info['player_id'] == node, 'country_of_citizenship'].values[0]

# Calculate homophily for nationality
same_nationality_edges = sum(
    1 for u, v in G.edges() if G.nodes[u]['nationality'] == G.nodes[v]['nationality']
)
total_edges = G.number_of_edges()
homophily_nationality = same_nationality_edges / total_edges
print(f"Homophily for nationality: {homophily_nationality:.2f}")

# Degree assortativity
assortativity_degree = nx.degree_assortativity_coefficient(G)
print(f"Degree assortativity coefficient: {assortativity_degree:.2f}")

# Function to get player information
def get_top_players_info(player_ids):
    player_data = []
    
    for player_id in player_ids:
        # Get the number of appearances of the player
        appearances = df[df['player_id'] == player_id].shape[0]
        
        # Get the number of different teams the player has played for
        teams_played_for = df[df['player_id'] == player_id]['player_club'].nunique()
        
        # Get the player's name
        name = players_info.loc[players_info['player_id'] == player_id, 'name'].values[0]
        
        # Get the nationality
        country = players_info.loc[players_info['player_id'] == player_id, 'country_of_citizenship'].values[0]
        
        # Get the market value
        total_market_value = player_valuations.loc[player_valuations['player_id'] == player_id, 'market_value_in_eur'].sum()
        
        # Get the position
        position = game_lineups.loc[game_lineups['player_id'] == player_id, 'position'].values[0]
        
        # Calculate the number of goals
        goals = game_events[(game_events['player_id'] == player_id) & (game_events['type'] == 'Goals')].shape[0]
        
        # Add the information to the list
        player_data.append({
            'player_id': player_id,
            'name': name,
            'country': country,
            'market_value_in_eur': total_market_value,
            'appearances': appearances,
            'position': position,
            'teams_played_for': teams_played_for,
            'goals': goals
        })
    
    # Convert to DataFrame for easier display
    return pd.DataFrame(player_data)

# Example usage with the 5 most central players
top_5_player_ids = [player_id for player_id, _ in top_5_players]
top_players_info = get_top_players_info(top_5_player_ids)
print(top_players_info)
print("\n")

top_5_player_ids_eigen = [player_id for player_id, _ in top_5_players_eigen]
top_players_info_eigen = get_top_players_info(top_5_player_ids_eigen)
print(top_players_info_eigen)
print("\n")

top_5_player_ids_betweenness = [player_id for player_id, _ in top_5_players_betweenness]
top_players_info_betweenness = get_top_players_info(top_5_player_ids_betweenness)
print(top_players_info_betweenness)
print("\n")

# Graph visualization (optional)
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)
weights = [G[u][v]['weight'] for u, v in G.edges()]
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue', alpha=0.7)
edges = nx.draw_networkx_edges(G, pos, width=2, edge_color=weights, edge_cmap=plt.cm.Blues)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'name'), font_size=2, font_weight='bold')
plt.title("Players network graph")
plt.colorbar(edges, label="Edge's weight (number of matches)")
plt.axis('off')
plt.show()
