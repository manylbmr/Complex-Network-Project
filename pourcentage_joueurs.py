import pandas as pd

# Charger la table players
players = pd.read_csv('reseaux_complexes/players.csv')

# Compter les occurrences de chaque nationalité
nationality_counts = players['country_of_citizenship'].value_counts()

# Obtenir les 10 nationalités les plus présentes
top_10_nationalities = nationality_counts.head(10)

# Calculer les pourcentages

total_players = len(players)
top_10_percentages = (top_10_nationalities / total_players) * 100

# Afficher les résultats
print("Pourcentage des 10 nationalités les plus présentes :")
print(top_10_percentages)
