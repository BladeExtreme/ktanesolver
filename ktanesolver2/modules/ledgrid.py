from ..edgework import edgework
from ..tools.colordict import _colorcheck

class ledgrid(edgework):
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g)!=3: raise IndexError("Length of grid must be 3")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==3 for a in g]): raise IndexError("Length of element of grid must be 3")
        elif not all([isinstance(a, str) for b in g for a in b]): raise TypeError("Each value of element of grid must be str")
        return [_colorcheck(a.lower()) for b in g for a in b]
    
    def __init__(self, edgework:edgework, grid:list):
        '''
        Initialize a new ledgrid instance

        Args:
            edgework (edgework): The edgework of the bomb
            colorgrid (list [str, ...]): The 2d color grid that appears on the module. Off LEDs should be notated with the color 'black'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)
    
    def __calculate(self):
        off = self.__grid.count('black')
        if off==0:
            if self.__grid.count('orange'): return ['C','D','A','B']
            elif self.__grid.count('red')>=3: return ['D','A','C','B']
            elif len([a for a in self.__grid if self.__grid.count(a)==2])>=2: return ['B','A','C','D']
            elif self.__grid[6]==self.__grid[7]==self.__grid[8]: return ['A','C','D','B']
            else: return ['B','C','D','A']
        elif off==1:
            if len(set(self.__grid))==len(self.__grid): return ['D','C','B','A']
            elif self.__grid[0]==self.__grid[1]==self.__grid[2]: return ['B','C','A','D']
            elif self.__grid.count('red')==3 or self.__grid.count('pink')==3 or self.__grid.count('purple')==3: return ['C','B','A','D']
            elif self.__grid.count('white')==1 or self.__grid.count('blue')==2 or self.__grid.count('yellow')==3: return ['B','A','D','C']
            else: return ['D','B','A','C']
        elif off==2:
            if self.__grid.count('purple')>=3: return ['A','D','C','B']
            elif len([a for a in self.__grid if self.__grid.count(a)==2])==2: return ['B','C','A','D']
            elif self.__grid.count('white')>=1 and self.__grid.count('orange')>=1 and self.__grid.count('pink')>=1: return ['D','B','C','A']
            elif self.__grid.count('green')==1 or self.__grid.count('yellow')==2 or self.__grid.count('red')==3 or self.__grid.count('blue')==4: return ['C','A','D','B']
            else: return ['C','D','B','A']
        elif off==3:
            if self.__grid.count('orange')==2: return ['B','D','A','C']
            elif len([a for a in self.__grid if self.__grid.count(a)==2])>1: return ['C','A','D','B']
            elif self.__grid.count('purple')==0: return ['D','C','A','B']
            elif self.__grid.count('red')>=1 and self.__grid.count('yellow')>=1: return ['A','C','D','B']
            else: return ['B','D','C','A']
        elif off==4:
            if self.__grid[3]==self.__grid[4]==self.__grid[5]: return ['B','C', 'D','A']
            elif self.__grid.count('green')>=2: return ['A','B','D','C']
            elif len([a for a in self.__grid if self.__grid.count(a)==2])==2: return ['C','B','D','A']
            elif self.__grid.count('pink')==0: return ['D','A','B','C']
            else: return ['A','B','C','D']

    def solve(self):
        '''
        Solve the LED Grid module

        Returns:
            tuple (str): The letter press in that order. Index 0 is the first press and so on.
        '''
        return tuple(self.__calculate())