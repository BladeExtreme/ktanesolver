import copy
from ..edgework import edgework

class chordqualities(edgework):
    __notestep = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    __qualtoroot = [7, 8, 10, 5, 9, 1, 3, 4, 6, 0, 2, 11]
    __roottoqual = [5, 7, 2, 4, 10, 6, 0, 3, 8, 11, 9, 1]
    __table = [
        ['X','X','X','X','X','X','X','X','X','X','X','X'],
        ['-','-','-','-','-','-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','X','X','-','-','-','-'],
        ['-','X','-','X','X','X','-','X','-','-','-','X'],
        ['X','-','X','-','X','-','X','-','X','X','-','-'],
        ['-','-','-','-','-','-','-','-','-','-','X','-'],
        ['-','-','-','-','-','X','-','-','-','-','-','-'],
        ['X','X','X','X','-','-','X','X','-','-','X','-'],
        ['-','-','-','-','-','-','-','-','X','X','-','X'],
        ['-','-','-','-','-','-','-','-','-','-','-','-'],
        ['X','X','-','-','X','X','-','-','X','-','X','-'],
        ['-','-','X','X','-','-','-','-','-','X','-','X']
    ]
    
    def __check(self, m):
        if not isinstance(m, list): raise TypeError("marked_notes must be in list")
        elif not all([isinstance(a, str) for a in m]): raise TypeError("Element of marked_notes must be in str")
        elif not all([a.upper() in self.__notestep for a in m]): raise ValueError("Element of marked_notes must be one of these [C, C#, D, D#, E, F, F#, G, G#, A, A#, B]")
        distance = []
        
        for a in range(len(m)):
            temp = self.__notestep[:self.__notestep.index(m[a])]+self.__notestep[self.__notestep.index(m[a]):]
            distance.append(abs(temp.index(m[a])-temp.index(m[(a+1)%len(m)])))

        return distance, [a.upper() for a in m]
    
    def __init__(self, edgework:edgework, marked_notes:list[str]):
        '''
        Initialize a new chordqualities instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__distance, self.__marked = self.__check(marked_notes)
    
    def __calculate(self):
        lendist = len(self.__distance)
        root = ''; quality = ''
        for a in range(len(self.__marked)):
            if root!='': break
            for b in range(len(self.__table)):
                if self.__table[self.__distance[a]][b]=='X' and self.__table[(self.__distance[a]+self.__distance[(a+1)%lendist])%len(self.__table)][b]=='X' and self.__table[(self.__distance[a]+self.__distance[(a+1)%lendist]+self.__distance[(a+2)%lendist])%len(self.__table)][b]=='X':
                    root = self.__marked[a]
                    quality = b
                    break
        
        new_dist = []
        newroot = self.__notestep[self.__qualtoroot[quality]]
        for a in range(12):
            if self.__table[a][self.__roottoqual[self.__notestep.index(root)]]=='X': new_dist.append(self.__notestep[(self.__notestep.index(newroot)+a)%12])
        return new_dist

    def solve(self):
        '''
        Solve the Chord Qualities module

        Returns:
            tuple (str): The chord to be submitted
        '''
        return tuple(self.__calculate())