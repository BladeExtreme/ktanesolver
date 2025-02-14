from ..edgework import edgework
from ..tools.colordict import _colorcheck

class blindmaze(edgework):
    __maze = [
        [
	        ['14','1','230','14','12'],
	        ['24','34','1','23','24'],
	        ['34','12','34','12','234'],
	        ['14','2','124','34','12'],
	        ['234','23','23','134','23']
        ],[
        	["134","12","240","14","12"],
        	["24","34","1","23","24"],
        	["34","12","34","12","234"],
        	["14","2","124","34","12"],
        	["234","34","23","134","23"],
        ],[
        	["14","123","40","123","124"],
        	["34","13","3","13","2"],
        	["134","1","1","1","23"],
        	["124","24","24","34","12"],
        	["34","23","34","123","23"]
        ],[
        	["134","12","230","1","12"],
            ["14","3","13","23","24"],
            ["4","12","14","1","23"],
            ["234","234","24","4","12"],
            ["134","13","23","234","234"]
        ],[
        	["14","1","30","12","124"],
        	["234","24","124","34","2"],
        	["14","3","23","14","23"],
        	["24","134","12","34","12"],
        	["34","123","34","13","23"]
        ],[
        	["14","12","340","13","12"],
        	["24","4","123","14","23"],
        	["24","4","13","","12"],
        	["234","24","14","23","24"],
        	["134","23","34","123","234"]
        ],[
        	["14","1","30","13","12"],
        	["24","234","14","12","24"],
        	["24","134","23","4","2"],
        	["34","12","134","23","24"],
        	["134","3","123","134","23"]
        ],[
        	["134","12","240","124","124"],
        	["14","2","24","4","23"],
        	["24","34","2","34","12"],
        	["24","124","34","12","24"],
        	["234","34","13","3","23"],
        ],[
        	["14","13","20","14","123"],
        	["24","14","3","3","12"],
        	["24","34","123","134","2"],
        	["34","123","14","12","24"],
        	["134","13","23","34","23"]
        ],[
        	["124","134","20","14","12"],
        	["34","12","24","24","234"],
        	["124","34","3","","123"],
        	["4","12","14","","123"],
        	["234","34","23","34","234"]
        ]
    ]
    
    def __check(self, c, s, b):
        if not isinstance(c, dict): raise TypeError("color must be in dict")
        elif not all([isinstance(a, str) for a in c.keys()]): raise TypeError("Keys of color must be in str")
        elif not all([isinstance(a, str) for a in c.values()]): raise TypeError("Values of color must be in str")
        elif not all([a.lower() in ['n','e','w','s'] for a in c.keys()]): raise KeyError("Keys of color must be 'N','E','W','S'")
        elif not all([_colorcheck(a.lower()) in ['red','green','blue','gray','yellow'] for a in c.values()]): raise ValueError("Values of color must be 'red','green','blue','gray' or 'yellow'")
        elif not isinstance(s, int): raise TypeError("solved_modules must be in int")
        elif s<0: raise ValueError("solved_modules must be positive")
        elif not isinstance(b, bool): raise TypeError("other_module_name must be in bool")
        return {a.upper(): _colorcheck(b.lower()) for a,b in c.items()}, s, b
    
    def __init__(self, edgework:edgework, color:dict[str,str], other_module_name:bool=False, solved_modules:int=0):
        '''
        Initialize a blindmaze instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (dict [str, str]): The color of the 'N','E','W','S' buttons. Keys are the direction ('N','E','W','S') and the values of each direction is in str, representing a color
            other_module_name (bool): The state if there are other modules with the "maze" on its name aside from "Blind Maze". By default, this parameter value is False
            solved_moduels (int): The number of modules that has been solved. By default this parameter is 0
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__solved, self.__other_module = self.__check(color, solved_modules, other_module_name)
    
    def __rotating_maze(self, maze, rotation):
        self.__rotation = rotation
        for a in rotation:
            maze = [list(b)[::-1] for b in list(zip(*maze))]
            for c in range(len(maze)):
                maze[c] = ["".join(sorted([e if e in ['A','0'] else str(int(e)+1) if int(e)+1<5 else str(1) for e in d])) for d in maze[a]]
        return maze

    def __starting_coord(self, maze):
        table = {
            'N': [1,5,2,2,3],
            'E': [3,1,5,5,2],
            'W': [2,5,3,1,4],
            'S': [3,2,4,3,2]
        }
        color_table = {
            'red': 0, 'green': 1, 'blue': 2, 'gray': 3, 'yellow': 4
        }
        x = ((table.get('N')[color_table.get(self.__color['N'])]+table.get('S')[color_table.get(self.__color['S'])])-1)%5
        y = ((table.get('E')[color_table.get(self.__color['E'])]+table.get('W')[color_table.get(self.__color['W'])])-1)%5
        maze[y][x] = maze[y][x]+'A'
        return maze

    def __calculate(self):
        maze = self.__maze[(int(self._sndigit[-1])+self.__solved)%10]
        
        if len([a for a in self.__color.values() if a=="red"])>=2:
            maze = self.__starting_coord(self.__rotating_maze(maze, 1))
        elif self.batt>=5:
            maze = self.__rotating_maze(self.__starting_coord(maze), 1)
        elif "IND" in self.ind or "IND*" in self.ind:
            maze = self.__starting_coord(self.__rotating_maze(maze, 2))
        elif len([a for a in self.__color.values() if a=="yellow"])==0 and len([a for a in self.__color.values() if a=="red"])>=1:
            maze = self.__starting_coord(self.__rotating_maze(maze, 3))
        elif self.__other_module:
            maze = self.__rotating_maze(self.__starting_coord(maze), 2)
        elif len(self._uniqueports)==1:
            maze = self.__rotating_maze(self.__starting_coord(maze), 3)
        else:
            self.__rotation = 0
            maze = self.__starting_coord(maze)
        
        return self.__bfs(maze)
    
    def __bfs(self, maze):
        starting_coord = []
        for a in range(len(maze)):
            for b in range(len(maze[a])):
                if '0' in maze[a][b]:
                    starting_coord = [b,a]
                    break
        
        # Coord, Path
        queue = [[starting_coord, []]]
        visited = set()
        while queue:
            coord, path = queue.pop(0)
            if '0' in maze[coord[0]][coord[1]]:
                path.append({0:'u', 1: 'r', 2: 'd', 3:'l'}.get(self.__rotation))
                return path
            if tuple(coord) in visited: continue
            visited.add(tuple(coord))
            restriction = maze[coord[0]][coord[1]]
            neighbors = [a for a in 'uldr' if (a=='u' and '1' not in restriction) or (a=='r' and '2' not in restriction) or (a=='d' and '3' not in restriction) or (a=='l' and '4' not in restriction)]
            for a in neighbors:
                if a=='u': new_coord = [coord[0]-1, coord[1]]
                elif a=='r': new_coord = [coord[0], coord[1]+1]
                elif a=='d': new_coord = [coord[0]+1, coord[1]] 
                elif a=='l': new_coord = [coord[0], coord[1]-1]
                queue.append([new_coord, path+[a]])
        return None

    def solve(self):
        '''
        Solve the Blind Maze module

        Returns:
            tuple [str]: The path to the goal in tuple. Index 0 is the first move, and so on.
        '''
        result = self.__calculate(); table = {'u': "North", 'l': "West", 'r': "East", 'd': "South"}
        for a in range(len(result)):
            result[a] = table.get(result[a])
        return tuple(result)