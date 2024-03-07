"""
This is the graph module. It contains a minimalistic Graph class.
"""
from grid import Grid
import sys
sys.path.insert(1, "/Users/arthurbidel/Documents/ENSAE/Informatique/S2/ensae-prog24-1/swap_puzzle")

#fonction supplémentaire:

def make_hashable(item):
    """
    Recursive function that makes the interior of an array hashable

    Parameters:
    -----------
    item: int, list[int], tuple[int], list[list[int]], list[tuple[int]], etc.
        Element from un hashable types

    Output:
    -------
    item if item is an int.
    item as a tuple[int], tuple[tuple[int]], etc. It has the same length as item.
    """
    if not isinstance(item, int):
        return tuple(make_hashable(x) for x in item)  # Conversion récursive
    else:
        return item

class Graph():
    """a
    A class representing undirected graphs as adjacency lists.

    Attributes:
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type,
        e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges.
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, n, m):
        """
        Initializes the graph with a set of nodes, and no edges.

        Parameters:
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        nodes = Grid(n, m).all_states()
        self.nodes = nodes
        self.graph = dict([(i, []) for i in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        self.n = n
        self.m = m

    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"
        else:
            output = (f"The graph has {self.nb_nodes} nodes "
                      f"and {self.nb_edges} edges.\n")
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self):
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return (f"<graph.Graph: nb_nodes={self.nb_nodes},"
                f"nb_edges={self.nb_edges}>")

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented,
        hence an edge is added to the adjacency list of both end nodes.
        When adding an edge between two nodes,
        if one of the ones does not exist it is added to the list of nodes.

        Parameters:
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        if node2 not in  self.graph[node1]:
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
            self.nb_edges += 1
            self.edges.append((node1, node2))

    def add_neighbours(self):
        ''' On va créer les edges de notre graph, qui n'est défini que par la taille des grilles. On parcours tous les états, soit tous les nœuds et on ajoute les voisins dans les edges, il y a plusieurs boucles for qui ne servent qu'a alterner entre tuple et liste afin d'avoir le bon format pour les bonnes méthodes. '''
        for tuples in Grid(self.n, self.m).all_states():
            # passage de la grille en liste pour la méthode all_neighbours
            grille = list(tuples)
            for i in range(self.n):
                grille[i] = list(grille[i])

            grille1 = Grid(self.n, self.m, grille)

            node1 = grille1.state
            for vosin in grille1.all_neighbours():
                node2 = vosin 
                # passage en tuple pour add_edge
                for i in range(self.n):
                    node1[i] = tuple(node1[i])

                self.add_edge(tuple(node1), tuple(node2))
                # repassage en liste pour la boucle 
                for i in range(self.n):
                    node1[i] = list(node1[i])
        return None


    def add_node (self, node):
        if node not in self.graph:
            self.graph[node] = []
            self.nb_nodes += 1
            self.nodes.append(node)


    def bfs(self, src, dst):
        queue = [src]  # Utilise une liste pour stocker les nœuds à explorer
        visited = set([src])  # Utilise un ensemble pour garder une trace des nœuds déjà visités
        paths = [[src]]  # Liste pour stocker les chemins

        while queue: #tant que cette liste n'est pas vide
            current_size = len(queue)  # Nombre de nœuds à explorer à ce niveau
            new_paths = []  # Pour stocker les nouveaux chemins générés à ce niveau

            while current_size > 0:
                current_node = queue.pop(0)  # Récupère le premier nœud de la queue
                current_path = paths.pop(0)  # Récupère le chemin correspondant

                if current_node == dst:
                    return current_path  # Retourne le chemin trouvé dès la première solution

                for neighbor in self.graph[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)  # Marque le voisin comme visité
                        queue.append(neighbor)  # Ajoute le voisin à la queue pour exploration
                        new_paths.append(current_path + [neighbor])  # Génère le nouveau chemin

                current_size -= 1  # Décrémente le compteur du niveau actuel

            paths.extend(new_paths)  # Ajoute les nouveaux chemins à la liste des chemins pour l'exploration suivante

        return []  # Retourne une liste vide si aucun chemin n'est trouvé


   """
    Question 7 :
    - Il faut d'abord construire le graphe de tous
    les états possible de la grille.
    > Pour cela, il faut créer un dictionaire
    avec pour chaque clé, un état de la grille,
     ie une des permutations
    > pour valeurs, ce sont tous les voisins
    d'un état de la grille, ie toutes
    les grilles accessibles par un swap.

    > L'algorithme BFS ci-dessus nous donne le chemin le plus court
    """

    # # def creer_dico_graph(self):
    #     """
    #     Question 8 :
    #     - Quelle est la partie du graphe nécessaire
    #     pour arriver au noeud de destination ?
    #     > On ne visite pas une nouvelle grille
    #     le swap qui permet de passer de l'une à l'autre est un swap qui:
    #     -> déplace un nombre sur une ligne qui l'éloigne de sa ligne dst
    #     -> déplace un nombre sur une colonne qui l'éloigne de sa colonne dst
    #     """



    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph
        as an object of the Graph class.

        The file should have the following format:
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters:
        -----------
        file_name: str
            The name of the file

        Outputs:
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2)  # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")

        return (graph)
    """
    Question 7 :
    - Il faut d'abord construire le graphe de tous
    les états possible de la grille.
    > Pour cela, il faut créer un dictionaire
    avec pour chaque clé, un état de la grille,
     ie une des permutations
    > pour valeurs, ce sont tous les voisins
    d'un état de la grille, ie toutes
    les grilles accessibles par un swap.

    > L'algorithme BFS ci-dessus nous donne le chemin le plus court
    """

    # # def creer_dico_graph(self):
    #     """
    #     Question 8 :
    #     - Quelle est la partie du graphe nécessaire
    #     pour arriver au noeud de destination ?
    #     > On ne visite pas une nouvelle grille
    #     le swap qui permet de passer de l'une à l'autre est un swap qui:
    #     -> déplace un nombre sur une ligne qui l'éloigne de sa ligne dst
    #     -> déplace un nombre sur une colonne qui l'éloigne de sa colonne dst
    #     """

    def bfs(self, src, dst):
        i = 0
        queue = [src]
        liste = [src]
        paths = [[src]]
        solution = []
        while i == 0:
            for node in self.graph[queue[0]]:
                if (node not in liste):
                    queue.append(node)
                    liste.append(node)
                    for path in paths:
                        if queue[0] in path:
                            paths.append(path.append(node))
            for path in paths:
                if dst in path:
                    i = 1
                    solution.append(path)
            queue.pop(0)
            i = 1
        return solution
