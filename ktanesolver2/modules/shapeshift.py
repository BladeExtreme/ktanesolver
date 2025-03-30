from ..edgework import edgework

class shapeshift(edgework):
    __shapedict = {'f':0, 'p':1, 'r':2, 't':3}
    __revshdict = {0: 'flat', 1:'point', 2:'round', 3:'ticket'}
    
    def __flowchart(self, n):
        flowchart = {
            0: 4 if int(self._sndigit[-1])%2==1 else 6,
            1: 13 if 'MSA*' in self._litind else 4,
            2: 9 if 'DVI-D' in self._uniqueports else 13,
            3: 14 if 'BOB' in self._unlitind else 5,
            4: 14 if 'CAR' in self._unlitind else 11,
            5: 7 if 'IND*' in self._litind else 0,
            6: 1 if 'PARALLEL' in self._uniqueports else 8,
            7: 9 if 'RJ-45' in self._uniqueports else 10,
            8: 10 if 'SND*' in self._litind else 11,
            9: 15 if 'SIG*' in self._litind else 0,
            10: 15 if any([a in ['a','i','u','e','o'] for a in self._snletter]) else 2,
            11: 12 if self.batt-self.hold != 0 else 3,
            12: 2 if 'FRQ' in self._unlitind else 5,
            13: 2 if 'PS/2' in self._uniqueports else 6,
            14: 1 if 'STEREO RCA' in self._uniqueports else 8,
            15: 12 if self.batt >= 3 else 3
        }
        return flowchart[n]
    
    def __check(self, s):
        if not isinstance(s, list): raise TypeError("Shape must be in list")
        elif len(s) != 2: raise IndexError("Length of shape must be 2")
        elif any([True if not isinstance(a, str) else False for a in s]): raise TypeError("Shapes in the list must be in str")
        temp = [self.__shapedict[a[0].lower()] if len(a) >1 else self.__shapedict[a.lower()] for a in s]
        return (temp[0]*4)+temp[1]
    
    def __init__(self, edgework:edgework, shape:list):
        '''
        Initialize a new Shape Shift instance

        Args:
            edgework (edgework): The edgework of the bomb
            shape (list [str, str]): The shape of each half. Index 0 is the left half and index 1 is the right half. Accepts 'round', 'flat', 'point', 'ticket'
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__shape = self.__check(shape)
    
    def __calculate(self):
        vis = [self.__shape]
        n = self.__flowchart(self.__shape)
        while n not in vis:
            vis.append(n)
            n = self.__flowchart(n)
        return n

    def solve(self):
        '''
        Solve the Shape Shift module

        Returns:
            Tuple (str, str): The correct shape to be submitted, index 0 represents the left half and index 1 represents the right half
        '''
        ans = self.__calculate()
        return tuple([self.__revshdict[(ans-(ans%4))/4], self.__revshdict[ans%4]])