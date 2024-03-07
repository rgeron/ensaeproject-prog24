"""
This is the graph module. It contains a minimalistic Graph class.
"""

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

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges.

        Parameters:
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []

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
        #on les transforme en tuples
        node1_h = make_hashable(node1)
        node2_h = make_hashable(node2)


        if node1_h not in self.graph:
            self.graph[node1_h] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2_h not in self.graph:
            self.graph[node2_h] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1_h].append(node2)
        self.graph[node2_h].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))


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