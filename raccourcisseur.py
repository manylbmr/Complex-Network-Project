import pandas as pd

# Charger le fichier CSV
file_path = 'C:/Users/bouma/intelligencia Comp/Travail 1/reseaux_complexes/appearances1.csv'  # Chemin de votre fichier CSV
output_path = "appearances_reduced.csv"  # Chemin pour le fichier réduit

# Lire le fichier
print("Chargement des données...")
df = pd.read_csv(file_path)

# Filtrer les lignes avec competition_id = GB1
df = df[df['competition_id'] == 'GB1']
print(f"Nombre total de lignes après filtrage : {len(df)}")

# Calculer la taille cible (20% des lignes restantes)
target_size = int(len(df) *1)
print(f"Nombre de lignes après réduction : {target_size}")

# Réduction aléatoire des données
df_reduced = df.sample(n=target_size, random_state=42)  # `random_state` pour des résultats reproductibles

# Sauvegarder le fichier réduit
df_reduced.to_csv(output_path, index=False)
print(f"Fichier réduit sauvegardé sous : {output_path}")
