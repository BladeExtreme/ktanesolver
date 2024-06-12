from ..edgework import edgework
from ..tools.colordict import _colorcheck

class minesweeper(edgework):
    __table = {
        'red': 5, 'orange': 2, 'yellow': 3,
        'green': 1, 'blue': 6, 'purple': 4
    }

    def __check(self, c):
        if not isinstance(c, list): raise TypeError("colors must be in list")
        elif not all([isinstance(a, str) for a in c]): raise IndexError("Element of colors must be in str")
        return [_colorcheck(a) for a in c]
    
    def __init__(self, edgework:edgework, colors:list):
        '''
        Initialize a new minesweeper instance

        Args:
            edgework (edgework): The edgework of the bomb
            colors (list [str, ...]): The colored squares that appears on the module in reading order. Index 0 represents color that appears on the most top and left than the other squares.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__colors = self.__check(colors)
    
    def __calculate(self):
        start = int(self._sndigit[1])%len(self.__colors) if int(self._sndigit[1])!=0 else 10%len(self.__colors)
        multiplier = self.__table[self.__colors[start-1]]
        temp = ((int(ord(self._snletter[0])-64)+multiplier)%len(self.__colors))-1
        reversed = self.__colors[::-1]
        return reversed[temp]

    def solve(self):
        '''
        Find the starting square to dig

        Returns:
            str: The colored square to press first
        '''
        return self.__calculate()