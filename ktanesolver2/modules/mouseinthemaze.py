from ..edgework import edgework
from ..tools.colordict import _colorcheck
from ..images.mouseinthemaze.image_loader import _loadimage

class mouseinthemaze(edgework):
    __ring2torus = [
        {'blue': 'white','yellow': 'yellow','white': 'green','green': 'blue'},
        {'yellow': 'blue','white': 'yellow','blue': 'white','green': 'green'},
        {'white': 'green','blue': 'yellow','green': 'blue','yellow': 'white'},
        {'white': 'blue','yellow': 'yellow','blue': 'green','green': 'white'},
        {'white': 'yellow','green': 'white','yellow': 'blue','blue': 'green'},
        {'white': 'blue','blue': 'green','green': 'yellow','yellow': 'white'}
    ]
    
    def __check(self, m, t):
        if not isinstance(m, int): raise TypeError("maze must be int int")
        elif not isinstance(t, str): raise TypeError("torus must be in str")
        elif _colorcheck(t.lower()) not in ['blue','yellow','white','green']: raise ValueError("Color of torus must be either 'blue', 'yellow', 'white', or 'green'")
        elif m not in range(0,6): raise ValueError("Value of maze must be in range of 0-5")
        return m,_colorcheck(t.lower())
    
    def __init__(self, edgework:edgework, maze:int|None=None, torus:str|None=None):
        '''
        Initialize a mouseinthemaze instance

        Args:
            edgework (edgework): The edgework of the bomb
            maze (int|None): The maze that is being used in the module represented by a number 0-5. Use showMazes() to see which maze is being used and what number it used to be represented as. By default, this value is None.
            torus (str|None): The color of the torus on the maze. By default, this value is None.
        
        NOTE:
            maze and torus must be both None or not None. Neither can be None and the other str/int
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if (maze is None) ^ (torus is None):
            raise TypeError(f"mouseinthemaze.__init__() missing 1 required positional argument: \'{'maze' if maze is None else 'torus'}\'")
        if maze is not None and torus is not None:
            self.__maze, self.__torus = self.__check(maze, torus)
        else:
            self.__maze = None; self.__torus = None
        
    def showMazes(self, maze_n:int|None=None):
        '''
        Show the mazes as well what number it represent

        Args:
            maze_n (int|None): To display one maze only according to that number. By default this value is None, which will display all mazes instead
        '''
        if maze_n is not None:
            if not isinstance(maze_n, int): raise TypeError("maze_n must be int")
            elif maze_n not in range(0,6): raise IndexError("maze_n must be in range of 0-5")
        else: maze_n = [a for a in range(6)]
        _loadimage(maze_n)
    
    def __calculate(self):
        return self.__ring2torus[self.__maze][self.__torus]

    def solve(self, starting_ring:str|None=None):
        '''
        Find the correct ring to submit on/Solve the Maze in the Mouse module

        # Args:
        #     starting_ring (str|None): The start ring of your assumed position. When this is parameter is not None, this function will return a pathfinding solution. Else, it will return the correct ring color. By default, this parameter is None
        
        Returns:
            str: The correct ring to be submitted on if the parameter starting_ring is None
            # list [str]: The correct path from the starting ring to the correct ring, assuming the initial direction is the north of the image (use showMazes())
        '''
        if self.__maze is None and self.__torus is None:
            raise TypeError("mouseinthemaze.__init__() missing 2 required positional argument: 'maze' and 'torus'")
        return self.__calculate()