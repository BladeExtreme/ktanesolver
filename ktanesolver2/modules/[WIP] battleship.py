from ..edgework import edgework

class battleship(edgework):
    def __check(self,c,r,p):
        if not isinstance(c, list): raise TypeError("col must be in list")
        elif not isinstance(r, list): raise TypeError("row must be in list")
        elif not isinstance(p, dict): raise TypeError("shippiece must be in dict")
        elif len(c)!=5: raise IndexError("Length of col must be 5")
        elif len(r)!=5: raise IndexError("Length of row must be 5")
        elif not all([a in [1,2,3,4] for a in p]): raise KeyError("shippiece key must consists of: 1, 2, 3, 4")
        elif not all([isinstance(a, int) for a in p.values()]): raise KeyError("Values of shippiece must be int")
        elif not all([isinstance(a, int) for a in c]): raise TypeError("Element of col must be int")
        elif not all([isinstance(a, int) for a in r]): raise TypeError("Element of row must be int")
        elif not all([a in range(0,5) for a in c]): raise ValueError("Value of col must be in range 1-4")
        elif not all([a in range(0,5) for a in r]): raise ValueError("Value of row must be in range 1-4")
        return c,r,p
    
    def __init__(self, edgework:edgework, col:list, row:list, shippiece:dict):
        '''
        Initialize a new battleship instance

        Args:
            edgework (edgework): The edgework of the bomb
            col (list (int)): The column numbers
            row (list (int)): The row numbers
            shippiece (dict (int)): The total amount of n-piece ships. Keys of dict are consists only the following: 1, 2, 3, 4. Each representing the n-ship pieces. Values of each key should reprersent how many ships of that piece are present
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__col, self.__row, self.__shippiece = self.__check(col, row, shippiece)
    
    def __calculate(self):
        pass
    
    def solve(self):
        return self.__calculate()