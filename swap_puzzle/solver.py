import numpy as np
from grid import Grid
import sys
sys.path.insert(1, "/Users/arthurbidel/ensae-prog24/swap_puzzle")


class Solver():
    """
    A solver class, to be implemented.
    """

    def __init__(self, m, n, initial_state):
        self.grid = Grid(m, n, initial_state)
        self.n = n
        self.m = m

    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        Allswap = []
        for i in range(1, self.m*self.n+1):
            j = 0  # indicatrice
            m_i = 0  # variable parcourant les lignes
            while j == 0:
                for n_j in range(self.n):  # parcours les colonnes sur la ligne
                    if self.grid.state[m_i][n_j] == i:
                        # test si on est sur le bon chiffre
                        n_i = n_j
                        # fixe la coordonnée de colonne si on est sur la bonne
                        m_i += -1
                        # corrige le décalage qu'il y a avec l'ajout final
                        j = 1
                m_i += 1

            # maintenant on a les coordonnées (m_i, n_i) du i-ème
            # chiffre du puzzle
            # On trouve les coordonnées dans la grille résolue
            m_is = int((i-1)//self.n)
            n_is = int((i-1) % self.n)

            if (m_is, n_is) != (m_i, n_i):
                d_ni = np.abs(n_is-n_i)  # calcul de la distance entre
                # la colonne d'arrivée et celle de départ
                s_ni = (n_is-n_i)/np.abs(n_is-n_i)
                # trouve le sens dans lequel
                # il faut aller
                for k in range(d_ni):
                    self.grid.swap((int(m_i), int(n_i+s_ni*k)),
                                   (int(m_i), int(n_i + s_ni*(k+1))))
                    Allswap.append(([m_i, n_i+s_ni*k],
                                    [m_i, n_i + s_ni*(k+1)]))
                    print(np.array(self.grid.state), "\n")

                d_mi = np.abs(m_is-m_i)
                # calcul de la distance entre les lignes
                for k in range(d_mi):
                    self.grid.swap((int(m_i-k), int(n_is)),
                                   (int(m_i-k-1), int(n_is)))
                    Allswap.append(([m_i-k, n_is], [m_i-k-1, n_is]))
                    print(np.array(self.grid.state),  "\n")
        return (Allswap, len(Allswap))
