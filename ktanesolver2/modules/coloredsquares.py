from ..edgework import edgework
from ..tools.colordict import _colorcheck

class coloredsquares(edgework):
    __table = [
        ['blue', 'column', 'red', 'yellow', 'row', 'green', 'magenta'],
        ['row', 'green', 'blue', 'magenta', 'red', 'column', 'yellow'],
        ['yellow', 'magenta', 'green', 'row', 'blue', 'red', 'column'],
        ['blue', 'green', 'yellow', 'column', 'red', 'row', 'magenta'],
        ['yellow', 'row', 'blue', 'magenta', 'column', 'red', 'green'],
        ['magenta', 'red', 'yellow', 'green', 'column', 'blue', 'row'],
        ['green', 'row', 'column', 'blue', 'magenta', 'yellow', 'red'],
        ['magenta', 'red', 'green', 'blue', 'yellow', 'column', 'row'],
        ['column', 'yellow', 'red', 'green', 'row', 'magenta', 'blue'],
        ['green', 'column', 'row', 'red', 'magenta', 'blue', 'yellow'],
        ['red', 'yellow', 'row', 'column', 'green', 'magenta', 'blue'],
        ['column', 'blue', 'magenta', 'red', 'yellow', 'row', 'green'],
        ['row', 'magenta', 'column', 'yellow', 'blue', 'green', 'red'],
        ['red', 'blue', 'magenta', 'row', 'green', 'yellow', 'column'],
        ['column', 'row', 'column', 'row', 'column', 'row', 'column']
    ]
    __col2idx = {
        'red': 0, 'blue': 1, 'green': 2,
        'yellow': 3, 'magenta': 4, 'row': 5,
        'column': 6
    }

    def __check(self, c, t):
        if not isinstance(c, str): raise TypeError("startingcolor must be in str")
        elif not isinstance(t, int): raise TypeError("total must be in int")
        elif t<=0: raise ValueError("total must be 1 or above")
        if c=='row' or c=='column': return c, t
        return _colorcheck(c), t
    
    def __init__(self, edgework:edgework):
        '''
        Initialize a new coloredsquares instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__pressed = 0
    
    def __calculate(self):
        if not self.__state: self.__pressed=self.__total
        else: self.__pressed += self.__total
        use = self.__table[self.__pressed-1][self.__col2idx[self.__color]]
        return use

    def solve(self, startingcolor:str, total:int|None=None, amount:int|None=None):
        '''
        Solve the Colored Squares module

        Args:
            startingcolor (str): The color group containing the fewest square
            total (int): The total number of squares where its color group contians the fewest number of squares
            amount (int): The amount of squares just pressed
        Returns:
            str: The color/state to press
        '''
        if total==None and amount==None: raise TypeError("coloredsquares.__init__() missing 1 required positional argument: total | amount")
        self.__color, self.__total = self.__check(startingcolor.lower(), total if amount==None else amount)
        self.__state = False if amount==None else True
        return self.__calculate()