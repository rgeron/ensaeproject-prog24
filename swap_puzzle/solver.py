from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.

    """
    
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """

    Solution = [] #liste où on va mettre les bons swaps

    While not self.grid.is_sorted:
        for i in range(self.m):
            for j in range(self.n):
                ???
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
        raise NotImplementedError

