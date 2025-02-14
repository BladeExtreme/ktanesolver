import copy
from ..edgework import edgework

class countdown(edgework):
    def __check(self, t, o):
        if not isinstance(t, int): raise TypeError("target must be int")
        elif not isinstance(o, list): raise TypeError("options must be in list")
        elif not all([isinstance(a, int) for a in o]): raise TypeError("Element of options must be int")
        elif len(o)!=6: raise IndexError("Length of options must be 6")
        return t,o
    
    def __init__(self, edgework:edgework, target:int, options:list[int]):
        '''
        Initialize a new countdown instance

        Args:
            edgework (edgework): The edgework of the bomb
            target (int): The target number to achieve
            options (list [int]): List of all numbers to be used in an operation'
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__target, self.__options = self.__check(target, options)
    
    def __calculate(self):
        pass
    
    def solve(self):
        return self.__calculate()