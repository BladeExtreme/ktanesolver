import copy
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
        vis = []; start = [zero, self.__grid[zero].index(0)]
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

    def __calculatePath(self, grid, target=None):
        if target is None:
            unicorn_table = [
                [[[1,0,2],[0,0,0],[4,0,3]], [[1,0,2],[0,0,0],[3,0,4]], [[1,0,3],[0,0,0],[7,0,5]], [[1,0,3],[0,0,0],[5,0,7]]],
                [[[0,1,0],[4,0,2],[0,3,0]], [[0,1,0],[3,0,2],[0,4,0]], [[0,2,0],[8,0,4],[0,6,0]], [[0,2,0],[6,0,4],[0,8,0]]],
                [[[1,0,0],[0,2,0],[0,0,3]], [[0,0,3],[0,2,0],[1,0,0]], [[3,0,0],[0,2,0],[0,0,1]], [[0,0,1],[0,2,0],[3,0,0]]],
                [[[1,2,3],[0,4,0],[0,0,0]], [[1,0,0],[2,4,0],[3,0,0]], [[0,0,0],[0,4,0],[1,2,3]], [[0,0,1],[0,4,2],[0,0,3]]]
            ]
            rotated_grid = [list(a)[::-1] for a in list(zip(*grid))]
            row = [sum([b for b in self.__grid[a]]) for a in range(len(self.__grid))]
            col = [sum([b for b in rotated_grid[a]]) for a in range(len(rotated_grid))]

            row_n = 0; col_n = 0
            if row.count(max(row))>1: row_n=3
            else: row_n = row.index(max(row))
            if col.count(max(col))>1: col_n=3
            else: col_n = col.index(max(col))
            return self.__bfs(grid, unicorn_table[row_n][col_n])
        else:
            return self.__bfs(grid, [[1,2,3],[4,5,6],[7,8,0]])

    def __bfs(self, grid, target):
        queue = [[grid, []]]
        visited = set()
        flat_target = [x for y in target for x in y]
        idx = [a for a in range(len(flat_target)) if flat_target[a]!=0]

        while queue:
            curr_grid, path = queue.pop(0)
            flat_grid = [x for y in curr_grid for x in y]
            if all([flat_target[a]==flat_grid[a] for a in idx]): return path
            if tuple([tuple(a) for a in curr_grid]) in visited: continue
            visited.add(tuple([tuple(a) for a in curr_grid]))

            x,y = 0,0
            for a in range(len(curr_grid)):
                if 0 in curr_grid[a]:
                    x = curr_grid[a].index(0); y = a
                    break
            
            neighbors = []
            for a in [[1,0],[0,1],[-1,0],[0,-1]]:
                if y+a[0]<3 and y+a[0]>=0 and x+a[1]<3 and x+a[1]>=0:
                    neighbors.append([y+a[0],x+a[1]])
            for a in neighbors:
                new_grid = copy.deepcopy(curr_grid)
                temp = new_grid[a[0]][a[1]]
                new_grid[a[0]][a[1]] = new_grid[y][x]
                new_grid[y][x] = temp

                queue.append([new_grid, path+[f"{curr_grid[a[0]][a[1]]}"]])

    def solve(self, solve_grid:list[list[int]]|None=None):
        '''
        Find the skull or Solve the Mystic Square module

        Args:
            solve_grid (list [list [int]]): The current grid if the mystic square wants to be solved. By default, this parameter is None. NOTE: The knight must be found first, to avoid any illegal moves or impossible solutions

        Returns:
            tuple (int, int, str): The position where the skull is. Index 0 represents the square number where the skull is below it. Index 1 represents the index of the square in reading order. Index 2 represents the position name of where the skull is located
            list [int]: If solve_grid is not None, it will return the correct path to solve the module
        '''
        if solve_grid is None:
            return tuple(self.__calculate())
        else:
            result1 = self.__calculatePath(self.__check(solve_grid))
            # result2 = self.__calculatePath(self.__check(solve_grid), 'standard')
            return result1