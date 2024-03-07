from itertools import permutations
import numpy as np 

def all_states(n, m):

    # Crée la liste (1, 2, ..., n*m)
    numbers = range(1, n * m + 1)

    # Génére toutes les permutations de la liste
    all_permutations = permutations(numbers)

    # Génére tous les états

    # On fait une distinction lorsqu'il y a une seule ligne afin de ne pas avoir 
    # une matrice avec un élément qui est la ligne 
    if n == 1:
        all_states=[]
        for permutation in all_permutations:
            all_states.append(list(permutation))
        
    else:
        all_states=[] # variable stockant tous les états 
        for permutation in all_permutations: # parcours des permutations
            state=[] # variable où l'on va construire un état
            l=[] # variable où l'on va construire les lignes 
            for i in permutation: # parcour la permutaion 
                if len(l) == m: # si on a la ligne de la bonne taille 
                    state.append(l) # on l'ajoute à l'état 
                    l=[] # on la vide 
                    l.append(i) # et on ajoute l'élément que l'on traita
                else: # sinon on ne fait qu'ajouter l'élément
                    l.append(i)
            state.append(l) # comme le dernier élément complète la dernière ligne il faut l'ajouter 
            all_states.append(state) #on ajoute l'état à tous les états 
        
    return all_states


a= Grid(2,2, [[1,3], [2, 4]]) 
a.all_neighbours()
