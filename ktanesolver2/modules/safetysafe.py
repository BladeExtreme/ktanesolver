from ..edgework import edgework

class safetysafe(edgework):
    __table = [
        [8, 3, 4, 8, 9, 0], [10, 1, 3, 7, 3, 8], [2, 1, 1, 5, 3, 6], [11, 6, 11, 11, 7, 7], [0, 5, 5, 8, 2, 1], [4, 2, 7, 7, 1, 5], 
		[7, 4, 4, 2, 10, 5], [8, 3, 6, 6, 6, 5], [0, 11, 0, 0, 9, 10], [2, 11, 8, 0, 5, 6], [5, 2, 5, 1, 0, 4], [1, 9, 8, 11, 11, 11], 
		[1, 7, 9, 5, 6, 2], [9, 5, 1, 4, 4, 9], [5, 9, 8, 10, 2, 8], [3, 10, 9, 1, 9, 7], [4, 10, 6, 1, 4, 8], [8, 0, 4, 0, 6, 11], [9, 4, 0, 6, 3, 10], 
		[7, 6, 7, 11, 5, 3], [11, 9, 6, 3, 11, 1], [11, 11, 2, 8, 1, 0], [6, 0, 11, 6, 11, 2], [4, 2, 7, 2, 8, 10], [10, 7, 10, 10, 8, 9], 
		[3, 7, 1, 10, 0, 4], [7, 0, 3, 5, 8, 6], [9, 10, 10, 9, 1, 2], [2, 5, 11, 7, 7, 3], [10, 8, 10, 4, 10, 4], [6, 8, 0, 3, 5, 0], 
		[6, 3, 3, 3, 0, 11], [1, 1, 5, 2, 7, 3], [0, 6, 2, 4, 2, 1], [5, 4, 9, 9, 10, 7], [3, 8, 2, 9, 4, 9]
    ]
    
    def __init__(self, edgework:edgework):
        '''
        Initialize a new safetysafe instance

        Args:
            edgework (edgework): The edgework of the bomb    
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__offset = 0
    
    def __calculate(self):
        validlitind = [a for a in self._snletter if any([b for b in self._litind if a in b])]; validunlitind = [a for a in self._snletter if any([b for b in self._unlitind if a in b])]
        offset = len(self._uniqueports)*7 + len(validlitind)*5 + len(validunlitind)
        ans = [(self.__table[int(self.sn[a])+26][a]+offset)%12 if self.sn[a].isnumeric() else (self.__table[int(ord(self.sn[a])-65)][a]+offset)%12 for a in range(len(self.sn[:-1]))]
        ans.append((sum([self.__table[int(self.sn[a])+26][-1] if self.sn[a].isnumeric() else self.__table[int(ord(self.sn[a])-65)][-1] for a in range(len(self.sn))])+offset)%12)
        return ans

    def solve(self):
        '''
        Solve the Safety Safe module

        Returns:
            Tuple (int, ...): The correct rotation offset for each dial in reading order. Index 0 represents dial top left, index 2 represents dial top right, index 3 represents dial bottom left and so on.
        '''
        return tuple(self.__calculate())