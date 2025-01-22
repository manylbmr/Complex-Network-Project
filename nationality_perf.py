import pandas as pd

# Charger les fichiers CSV
appearances = pd.read_csv('reseaux_complexes/appearances_reduced.csv')
games = pd.read_csv('reseaux_complexes/games.csv')
players = pd.read_csv('reseaux_complexes/players.csv')

# Ajouter la nationalité à la table appearances via players

appearances = appearances.merge(players[['player_id', 'country_of_citizenship']], on='player_id')

# Calculer la diversité de nationalités par club
diversity_by_club = appearances.groupby('player_club')['country_of_citizenship'].nunique().reset_index()
diversity_by_club.columns = ['club_id', 'nationality_diversity']

# Afficher les résultats
print("Diversité des nationalités par club :")
print(diversity_by_club)


# Associer la diversité des clubs à la table des jeux
games = games.merge(diversity_by_club, left_on='home_club_id', right_on='club_id', suffixes=('_home', '_away'))
games = games.rename(columns={'nationality_diversity': 'nationality_diversity_home'})

games = games.merge(diversity_by_club, left_on='away_club_id', right_on='club_id', suffixes=('', '_away'))
games = games.rename(columns={'nationality_diversity_away': 'nationality_diversity_away'})

# Vérification des colonnes après fusion
print(games.columns)


# Calculer les performances en fonction de la diversité
games['home_performance'] = games['home_club_goals'] - games['away_club_goals']
games['away_performance'] = games['away_club_goals'] - games['home_club_goals']

# Séparer les équipes en fonction de la diversité élevée et faible
high_diversity_home = games[games['nationality_diversity_home'] > games['nationality_diversity_home'].median()]
low_diversity_home = games[games['nationality_diversity_home'] <= games['nationality_diversity_home'].median()]

# Calculer la performance moyenne
high_div_home_performance = high_diversity_home['home_performance'].mean()
low_div_home_performance = low_diversity_home['home_performance'].mean()

# Afficher les résultats
print(f"Performance moyenne des équipes à haute diversité à domicile : {high_div_home_performance:.2f}")
print(f"Performance moyenne des équipes à faible diversité à domicile : {low_div_home_performance:.2f}")

