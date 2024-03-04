from itertools import permutations

def create_grids(n, m):
    # Créer la liste (1, 2, ..., n*m)
    numbers = list(range(1, n * m + 1))

    # Générer toutes les permutations de la liste
    all_permutations = list(permutations(numbers))

    # Créer les grilles à partir des permutations
    grids = [list(permutation[i:i+m]) for permutation in all_permutations for i in range(0, len(permutation), m)]

    return grids

# Définir la taille de la grille mxn
m = 3
n = 4

# Appeler la fonction pour créer les grilles
result = create_grids(m, n)

# Afficher les résultats
for grid in result:
    for row in grid:
        print(row)
    print()
