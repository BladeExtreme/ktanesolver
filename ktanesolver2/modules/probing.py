from ..edgework import edgework

class probing(edgework):
    def __check(self, f):
        if not isinstance(f, list): raise TypeError("missingfreq must be in list")
        elif len(f)!=6: raise IndexError("Length of missingfreq must be 6")
        elif not all([isinstance(a, int) for a in f]): raise TypeError("Element of missingfreq")
        elif not all([a>0 for a in f]): raise ValueError("missingfreq cannot be negative")
        return [int(str(a)[0]) for a in f]

    def __init__(self, edgework:edgework, missingfreq:list):
        '''
        Initialize a new probing instance

        Args:
            edgework (edgework): The edgework of the bomb
            missingfreq (list (int)): The missing frequencies for each wires in reading order. Index 0 is top left, index 2 is top right, index 3 is bottom left
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__missingfreq = self.__check(missingfreq)
    
    def __calculate(self):
        ans = {'red': 0, 'blue': 1}
        if self.__missingfreq[0] in [1,2,6]: ans['red'] = self.__missingfreq.index(5)
        elif self.__missingfreq[4] in [1]: ans['red'] = 5
        else: ans['red'] = self.__missingfreq.index(6)
        if self.__missingfreq[4] in [2,5,6]: ans['blue'] = self.__missingfreq.index(2)
        else: ans['blue'] = self.__missingfreq.index(6)
        return ans

    def solve(self):
        '''
        Solve the Probing module

        Returns:
            dict ('red', 'blue'): The index of the wire to be connect. Keys are the required color plug to connect to, the values are the index of the wire to be connected
        '''
        return self.__calculate()