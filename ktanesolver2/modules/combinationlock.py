from ..edgework import edgework

class combinationlock(edgework):
    def __check(self, s):
        if not isinstance(s, int): raise TypeError("Solved must be in int")
        elif s<0: raise ValueError("Solved cannot be a negative integer")
        return s

    def __init__(self, edgework:edgework, solved:int):
        '''
        Initialize a new combinationlock instance

        Args:
            edgework (edgework): The edgework of the bomb
            solved (int): The amount of solved modules
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__solved = self.__check(solved)
    
    def __calculate(self):
        #does not support 2 factor
        n = []
        n.append((int(self._sndigit[-1])+self.__solved+self.batt)%20)
        n.append((self.total_modules+self.needy+self.__solved)%20)
        n.append(sum(n[0:])%20)
        return n

    def solve(self):
        '''
        Solve the Combination Lock module

        Returns:
            Tuple (int, int, int): The correct numbers to submit where index 0 represents the first digit
        '''
        return tuple(self.__calculate())