from ..edgework import edgework
from ..tools.colordict import _colorcheck

class simonsays(edgework):
    __rule = {
        True:{
            'red': ['blue', 'yellow', 'green'],
            'blue': ['red', 'green', 'red'],
            'green': ['yellow', 'blue', 'yellow'],
            'yellow': ['green', 'red', 'blue']
        },
        False: {
            'red': ['blue', 'red', 'yellow'],
            'blue': ['yellow', 'blue', 'green'],
            'green': ['green', 'yellow', 'blue'],
            'yellow': ['red', 'green', 'red']
        }
    }

    def __init__(self, edgework, color):
        '''
        Initialize a simonsays instance

        Args:
            color (list): The color flash sequence of the module
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color = self.__check([_colorcheck(a.lower()) for a in color])

    def __check(self, c):
        if not isinstance(c, list): raise TypeError("Color has an invalid type")
        elif len(c) <= 0: raise IndexError("Sequence total must be more than 1")
        return c

    def interactive(self, color: list):
        '''
        A quicker way to calculate the color flash's response

        Args:
            color (list): The color flash sequence of the module
        Returns:
            Tuple (str): The color press in sequence where index 0 is the first press
        '''
        self.__color = self.__check([_colorcheck(a.lower()) for a in color])
        return self.solve()

    def solve(self):
        '''
        Solve the Simon Says module

        Returns:
            Tuple (str): The color press in sequence where index 0 is the first press
        '''
        ans = [self.__rule[any([a for a in self.__color if a in ['a','i','u','e','o']])][b][2 if self.strikes >= 2 else self.strikes] for b in self.__color]
        return tuple(ans)
