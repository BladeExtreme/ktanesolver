from ..edgework import edgework

class mysticsquare(edgework):
    __table = [
        [1, 3, 5, 4, 6, 7, 2, 8],
        [2, 5, 7, 3, 8, 1, 4, 6],
        [6, 4, 8, 1, 7, 3, 5, 2],
        [8, 1, 2, 5, 3, 4, 6, 7],
        [3, 2, 6, 8, 4, 5, 7, 1],
        [7, 6, 1, 2, 5, 8, 3, 4],
        [4, 7, 3, 6, 1, 2, 8, 5],
        [5, 8, 4, 7, 2, 6, 1, 3]
        ]
    
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g)!=3: raise IndexError("Length of grid must be 3")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==3 for a in g]): raise IndexError("Length of each row must be 3")
        if None in [a for b in g for a in b]: g[[a for a in range(len(g)) if None in g[a]][0]][g[[a for a in range(len(g)) if None in g[a]][0]].index(None)] = 0
        if not all([isinstance(a,int) for b in g for a in b]): raise TypeError("Grid must consist of int (except for empty space which can be None)")
        elif 0 not in [a for b in g for a in b]: raise ValueError("Empty space must exist")
        return g
    
    def __init__(self, edgework:edgework, grid:list):
        '''
        Initialize a new mysticsquare instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list [list [int, ...]]): The number grid that appears on the module. On empty space, insert None or 0. Each list represents a row
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)
        self.__state = 0 if (int(self._sndigit[-1]) if int(self._sndigit[-1])!=0 else -1) in [self.__grid[0][0],self.__grid[0][2],self.__grid[2][0],self.__grid[2][2],self.__grid[1][1]] else 1
    
    def __calculate(self):
        using = [self.__table[a][self.__grid[1][1]-1] if self.__state==1 else self.__table[self.__grid[1][1]-1][a] for a in range(8)]
        zero = [a for a in range(len(self.__grid)) if 0 in self.__grid[a]][0]
        vis = []; start = [zero, self.__grid[zero][self.__grid[zero].index(0)]]
        for a in using:
            if self.__grid[start[0]][start[1]] not in vis: vis.append(self.__grid[start[0]][start[1]])
            neighbors = [[start[0]+1,start[1]],[start[0],start[1]+1],[start[0]-1,start[1]],[start[0],start[1]-1]]
            for b in neighbors:
                try:
                    if a == self.__grid[b[0]][b[1]]:
                        start = [b[0],b[1]]
                        break
                except: pass
        temp = [a for b in self.__grid for a in b].index(vis[-1])
        return vis[-1], temp, " ".join(['top' if int((temp-temp%3)/3)==0 else 'middle' if int((temp-temp%3)/3)==1 else 'bottom', 'left' if temp%3==0 else 'middle' if temp%3==1 else 'right'])

    def solve(self):
        '''
        Find the skull in the Mystic Square module

        Returns:
            int: The square number where the skull is below it
            int: The index of the square in reading order. 0 is top left and 8 bottom right
            str: The position name of where the skull is located
        '''
        return self.__calculate()