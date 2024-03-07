import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import permutations


class Grid():

    """
    A class representing the grid from the swap puzzle.
    It supports rectangular grids.

    Attributes:
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the
        number in the cell (i, j), i.e., in the i-th line and j-th column.
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """

    def __init__(self, m, n, initial_state=[]):
        """
        Initializes the grid.

        Parameters:
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty
            (then the grid is created sorted).
        """
        self.m = m
        self.n = n

        if not initial_state:  # si elle est vide on la crée ordonnnée
            # (car le booléen d'un objet vide est false)
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]

        self.state = initial_state  # on ne peut plus avoir de tableau vide

    def __str__(self):
        """
        Prints the state of the grid as text.
        """
        output = "The grid is in the following state:\n"
        for i in range(self.m):  # pour chaque ligne, on affiche toute la ligne
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self):
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorte and
        returns the answer as a boolean.
        """
        if self.state == Grid(self.m, self.n).state:
            # Grid(self.m,self.n).state -> renvoie la liste ordonnée car elle est passé par initial_state
            return True
        else:
            return False

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells.
        Raises an exception if the swap is not allowed.

        Parameters:
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j)
            where i is the line and j the column number of the cell.
        """

        if (np.abs(cell1[0]-cell2[0]) + np.abs(cell1[1]-cell2[1]) <= 1):
            # il faut qu'ils soient au moins sur la même ligne ou la même
            # colonne et à une case d'écart maximum.
            (self.state[cell1[0]][cell1[1]],
             self.state[cell2[0]][cell2[1]]) = (self.state[cell2[0]][cell2[1]],
                                                self.state[cell1[0]][cell1[1]])
            return None
        else:
            raise ValueError("The swap is not allowed")

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps.

        Parameters:
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells
            (each cell being a tuple of integers).
            So the format should be [((i1, j1), (i2, j2)),
              ((i1', j1'), (i2', j2')), ...].
        """
        for i in range(len(cell_pair_list)):
            self.swap(cell_pair_list[i][0], cell_pair_list[i][1])

        return None

    def rpzr(self):
        fig, ax = plt.subplots(1, 1)
        data = self.state
        ax.table(cellText=data, loc="center", cellLoc="center")
        plt.show()
        return None

    def all_states(self):  # Créer tous les états possibles
        # Crée la liste (1, 2, ..., n*m)
        numbers = range(1, self.n * self.m + 1)

        # Génére toutes les permutations de la liste
        all_permutations = permutations(numbers)

        # Génére tous les états

        # On fait une distinction lorsqu'il y a une seule ligne afin de
        # ne pas avoir une matrice avec un élément qui est la ligne
        if self.n == 1:
            all_states = []
            for permutation in all_permutations:
                all_states.append(list(permutation))

        else:
            all_states = []  # variable stockant tous les états
            for permutation in all_permutations:  # parcours des permutations
                state = []  # variable où l'on va construire un état
                ligne = []  # variable où l'on va construire les lignes
                for i in permutation:  # parcourt la permutaion (qui est une ligne)
                    if len(ligne) == self.n: #n est le nombre de colonne et donc la dimension d'une ligne
                        # si on a la ligne de la bonne taille
                        state.append(ligne)  # on l'ajoute à l'état
                        ligne = []  # on la vide
                        ligne.append(i)  # et on ajoute l'élément
                    else:  # sinon on ne fait qu'ajouter l'élément
                        ligne.append(i)
                state.append(ligne)  # comme le dernier élément complète la dernière ligne, il faut l'ajouter
                all_states.append(state)  # on ajoute l'état à tous les états

        return all_states

    def all_swaps(self):  # donne tous les swaps possibles sur une grille
        ''' L'idée est de parcourir tous les indices de la grille, en regardant
        pour chacune des lignes chacune des colones. Sur chaque élément
        on ne regarde au maximun que 2 swaps, celui à droite et celui en bas,
        comme ça on est sûr de ne pas recouper les swaps.'''
        indices_de_ligne = range(0, self.n)
        indices_de_colonne = range(0, self.m)
        all_swaps = []
        # avec les deux permiers for on parcours tous les indices
        for indice_1 in indices_de_ligne:
            for indice_2 in indices_de_colonne:
                position_1 = [indice_1, indice_2]
                # on ne swap vers le bas que si on est pas collé en bas
                if indice_1 < self.n - 1:
                    position_2 = [indice_1 + 1, indice_2]
                    all_swaps.append([position_1, position_2])
                if indice_2 < self.m - 1:  # de mêmeà droite
                    position_2 = [indice_1, indice_2 + 1]
                    all_swaps.append([position_1, position_2])
        return all_swaps


        @classmethod
        def grid_from_file(cls, file_name):
            """
            Creates a grid object from class Grid, initialized
            with the information from the file file_name.

            Parameters:
            -----------
            file_name: str
                Name of the file to load. The file must be of the format:
                - first line contains "m n"
                - next m lines contain n integers that
                represent the state of the corresponding cell

            Output:
            -------
            grid: Grid
                The grid
            """
            with open(file_name, "r") as file:
                m, n = map(int, file.readline().split())
                initial_state = [[] for i_line in range(m)]
                for i_line in range(m):
                    line_state = list(map(int, file.readline().split()))
                    if len(line_state) != n:
                        raise Exception("Format incorrect")
                    initial_state[i_line] = line_state
                grid = Grid(m, n, initial_state)
            return grid
