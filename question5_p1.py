import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import louvain_communities

# Load data
df = pd.read_csv('reseaux_complexes/appearances_reduced.csv')
players_info = pd.read_csv('reseaux_complexes/players.csv')
games = pd.read_csv('reseaux_complexes/games.csv')


# Initialize the graph
G = nx.Graph()

# Add nodes and edges
for club, club_group in df.groupby('player_club'):
    for game_id, game_group in club_group.groupby('game_id'):
        players = game_group[['player_id', 'player_name']].values.tolist()
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                player1_id, player1_name = players[i]
                player2_id, player2_name = players[j]
                if G.has_edge(player1_id, player2_id):
                    G[player1_id][player2_id]['weight'] += 1
                else:
                    G.add_edge(player1_id, player2_id, weight=1)
                G.nodes[player1_id]['name'] = player1_name
                G.nodes[player2_id]['name'] = player2_name

# Compute layout
pos = nx.spring_layout(G, seed=42)

# Step 1: Remarkable Clusters
communities = louvain_communities(G)
community_colors = {node: i for i, community in enumerate(communities) for node in community}
node_colors = [community_colors[node] for node in G.nodes()]

plt.figure(figsize=(12, 12))
nodes = nx.draw_networkx_nodes(G, pos, node_size=30, node_color=node_colors, cmap=plt.cm.rainbow, alpha=0.7)
labels = {node: G.nodes[node]['name'] for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=5, font_color='black')  # Initial adjusted size
plt.title("Remarkable Clusters (with player names)")
plt.colorbar(nodes)
plt.axis('off')
plt.show()

# Step 2: Top Performing Players
df = df.merge(games[['game_id', 'home_club_id', 'away_club_id', 'home_club_goals', 'away_club_goals']], on='game_id')

df['win'] = ((df['player_club'] == df['home_club_id']) & (df['home_club_goals'] > df['away_club_goals'])) | \
            ((df['player_club'] == df['away_club_id']) & (df['away_club_goals'] > df['home_club_goals']))

player_performance = df.groupby('player_id')['win'].sum()

for node in G.nodes():
    G.nodes[node]['performance'] = player_performance.get(node, 0)

performance_values = [G.nodes[node]['performance'] for node in G.nodes()]
plt.figure(figsize=(12, 12))
nodes = nx.draw_networkx_nodes(G, pos, node_size=30, node_color=performance_values, cmap=plt.cm.viridis, alpha=0.7)
nx.draw_networkx_labels(G, pos, labels, font_size=0, font_color='black')
plt.colorbar(nodes, label='Number of Wins')
plt.title("Top Performing Players (with names)")
plt.axis('off')
plt.show()

# Step 3: Homophily
for node in G.nodes():
    G.nodes[node]['nationality'] = players_info.loc[players_info['player_id'] == node, 'country_of_citizenship'].values[0]

nationality_colors = {nationality: i for i, nationality in enumerate(players_info['country_of_citizenship'].unique())}
node_colors = [nationality_colors[G.nodes[node]['nationality']] for node in G.nodes()]

plt.figure(figsize=(12, 12))
nodes = nx.draw_networkx_nodes(G, pos, node_size=30, node_color=node_colors, cmap=plt.cm.jet, alpha=0.7)
nx.draw_networkx_labels(G, pos, labels, font_size=0, font_color='black')
plt.colorbar(nodes)
plt.title("Homophily (by nationality, with names)")
plt.axis('off')
plt.show()
