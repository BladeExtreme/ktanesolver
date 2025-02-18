import random
from ..edgework import edgework
from ..tools import colordict

class sevendeadlysins(edgework):
    __table = [
        [0,1,1,0,1,0,0],
        [0,0,1,1,0,1,0],
        [0,0,0,1,1,0,1],
        [1,0,0,0,1,1,0],
        [0,1,0,0,0,1,1],
        [1,0,1,0,0,0,1],
        [1,1,0,1,0,0,0]
    ]
    __sinidx = ["Lust", "Gluttony", "Greed", "Sloth", "Wrath", "Envy", "Pride"]
    __sintocol = {
        "Lust": "Yellow",
        "Gluttony": "Blue",
        "Greed": "Red",
        "Sloth": "Pink",
        "Wrath": "Moss",
        "Envy": "Forest",
        "Pride": "Brown"
    }
    
    def __check(self, s):
        if not isinstance(s, list): raise TypeError("Sins must be in list")
        elif not all([isinstance(a, str) for a in s]): raise TypeError("Element of Sins must be in str")
        elif len(s)!=7: raise IndexError("Sins' length must be exactly 7")
        elif set([a.lower() for a in s])!={'envy', 'gluttony', 'greed', 'lust', 'pride', 'sloth', 'wrath'}: raise ValueError("One or more of the sin name is invalid")
        return [a.capitalize() for a in s]
    
    def __checkC(self, c):
        if not isinstance(c, list): raise TypeError("Colors must be in list")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of Colors must be in str")
        elif len(c)!=7: raise IndexError("Colors' length must be exactly 7")
        elif not all([colordict._colorcheck(a.lower()) for a in c]): raise ValueError("One or more of the color is invalid")
        sintocol = {
            'yellow': "Lust",
            'blue': "Gluttony",
            'red': "Greed",
            'pink': "Sloth",
            'moss': "Wrath",
            'forest': "Envy",
            'brown': "Pride"
        }
        return [sintocol.get(a) for a in c]
    
    def __init__(self, edgework:edgework, sins:list[str]|None=None, colors:list[str]|None=None):
        '''
        Initialize a new sevendeadlysins instance

        Args:
            edgework (edgework): The edgework of the bomb
            sins (list (str)): The list represents the order of sins on the bomb, where the position of each sin in the list is significant. Each consecutive pair of sins in the list are directly related to each other and represent adjacent sins on the bomb
            colors (list (str)): The color of each sin on the module. CAUTION: colors must be in sync with sins. NOTE: If sins is not provided, colors must be provided and behaves like sins
        '''
        if sins and colors==None: raise TypeError("AdjacentLetters.__init__() missing 1 required positional argument: 'colors' or 'sins'")
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if sins is not None:
            self.__sins = self.__check(sins)
        elif colors is not None:
            self.__sins = self.__checkC(colors)
        elif sins is None and colors is None:
            raise TypeError("AdjacentLetters.__init__() missing 1 required positional argument: 'sins' or 'colors'")
    
    def __bfs(self, start):
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if len(path)==7: return path
            sin_node = self.__sinidx.index(node)
            neighbors = []
            if len(path)==1:
                for a in [(self.__sins.index(node)+1)%7, (self.__sins.index(node)-1)%7]:
                    if self.__table[sin_node][self.__sinidx.index(self.__sins[a])]==1: neighbors.append(self.__sins[a])
            else:
                for a in self.__sins:
                    if (a not in path):
                        if self.__sins[(self.__sins.index(a)-1)%7] in path and self.__table[sin_node][self.__sinidx.index(a)]==1: neighbors.append(a)
                        elif self.__sins[(self.__sins.index(a)+1)%7] in path and self.__table[sin_node][self.__sinidx.index(a)]==1: neighbors.append(a)
            for a in neighbors:
                queue.append(path+[a])
        return None

    def __calculate(self):
        solus = []
        for a in self.__sins:
            path = self.__bfs(a)
            if path is not None: solus.append(path)
        return solus
    
    def solve(self, colors:bool|None=None):
        '''
        Solve the Seven Deadly Sins module

        Args:
            colors (bool|None): State if the colors of the sins are provided instead

        Returns:
            list (str): One of the possible sin paths to be submitted. Do note that the result list may be a bit random every generation
        '''
        solus = self.__calculate()
        if colors:
            for a in range(len(solus)):
                solus[a] = [self.__sintocol.get(solus[a][b]) for b in range(len(solus[a]))]
        return solus[random.randint(0, len(solus)-1)]