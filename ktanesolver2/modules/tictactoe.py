from ..edgework import edgework

class tictactoe(edgework):
    __table = [
        [[9,3],[3,9],[8,1]],
        [[5,6],[6,7],[1,2]],
        [[7,8],[2,1],[5,8]],
        [[4,5],[7,8],[9,6]],
        [[1,4],[1,6],[7,3]],
        [[8,7],[5,2],[4,4]],
        [[6,1],[8,4],[3,9]],
        [[2,2],[9,5],[2,5]],
        [[3,9],[4,3],[6,7]]
    ]
    
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g)!=3: raise IndexError("Length of grid must be 3")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==3 for a in g]): raise IndexError("Length of grid's sublists must be 3")
        elif not all([isinstance(a, str) for b in g for a in b]): raise TypeError("Each element of grid's sublists must be in str")
        return [[b.upper() for b in a] for a in g]
    
    def __init__(self, edgework:edgework, grid:list):
        '''
        Initialize a new tictactoe instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list (str)): The initial tic-tac-toe grid on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)
        self.__numbers = [a for b in self.__grid for a in b if a.isnumeric()]
        self.__startingrow = self.__precalculate()
    
    def __precalculate(self):
        rangeset = range(5,10) if int(self._sndigit[-1])%2==0 else range(1,5)
        startingrow = [x for x in rangeset]
        if 'PARALLEL' in self._uniqueports: startingrow = [x for x in startingrow if x%2==0]
        else: startingrow = [x for x in startingrow if x%2==1]
        if len(self._litind)<len(self._unlitind): startingrow = min(startingrow)
        elif len(self._litind)>len(self._unlitind): startingrow = max(startingrow)
        else: startingrow = int(sum(startingrow)/len(startingrow))
        return startingrow-1

    def __does_not_win(self, num, n):
        gridcopy = [[b for b in a] for a in self.__grid]
        for a in range(len(self.__grid)):
            if num in self.__grid[a]: 
                x=gridcopy[a].index(num)
                y=a
                gridcopy[a][gridcopy[a].index(num)] = n; break
        try:
            if len(set(gridcopy[y]))==1: return False
            if len(set([a[x] for a in gridcopy]))==1: return False
            if len(set([gridcopy[0][0], gridcopy[1][1], gridcopy[2][2]]))==1 and ((x==0 and y==0) or (x==2 and y==2) or (x==1 and y==1)): return False
            if len(set([gridcopy[2][0], gridcopy[1][1], gridcopy[0][2]]))==1 and ((x==2 and y==0) or (x==0 and y==2) or (x==1 and y==1)): return False
            return True
        except:
            return False

    def __calculate(self, n):
        ans = None; ocount = [a for b in self.__grid for a in b].count('O'); xcount = [a for b in self.__grid for a in b].count('X')
        colouter = 0 if xcount>ocount else 1 if xcount==ocount else 2
        colinner = 0 if n=='X' else 1
        for x in range(len(self.__table)):
            i = str(self.__table[self.__startingrow][colouter][colinner])
            if i in self.__numbers:
                if not self.__does_not_win(i, n): return 'pass'
                for a in range(len(self.__grid)):
                    if i in self.__grid[a]:
                        ans = tuple([a, self.__grid[a].index(i)])
                        self.__grid[a][self.__grid[a].index(i)] = n; self.__numbers.pop(self.__numbers.index(i)); break
            self.__startingrow = (self.__startingrow+1)%9
            if ans is not None: return ans

    def solve(self, nextpiece:str, newpieceingrid:str|None=None, coord:tuple|None=None, striked:bool|None=False):
        '''
        Solve the Tic Tac Toe module

        Args:
            nextpiece (str): The next piece that comes up in the module
            newpieceingrid (str): The new piece created by the board if the board stalemates for a couple of rounds
            coord (tuple (int, int)): The coordinates of the new piece created by the board. Index 0 is the row, index 1 is the column
        Returns:
            tuple|str: The correct action to take, either 'pass' or a coordinate of a button in the grid. In tuple, index 0 is the row and index 1 is the column.
        '''
        if newpieceingrid is not None and coord is not None:
            if not isinstance(newpieceingrid, str): raise TypeError("newpieceingrid must be in str")
            elif newpieceingrid.upper() not in ['O','X']: raise ValueError("newpieceingrid must be either 'O' or 'X'")
            elif not isinstance(coord, tuple): raise TypeError("coord must be in tuple")
            elif len(coord)!=2: raise IndexError("Length of coord must be 2")
            elif not all([isinstance(a,int) for a in coord]): raise TypeError("Element of coord must be int")
            elif not all([a in range(0,3) for a in coord]): raise ValueError("Value of coord must be between 0-2")
            self.__grid[coord[0]][coord[1]] = newpieceingrid
            self.__numbers = [a for b in self.__grid for a in b if a.isnumeric()]
        if striked is not None:
            if not isinstance(striked, bool): raise TypeError("striked must be in bool")
            if striked: self.__startingrow = self.__precalculate()
        if not isinstance(nextpiece, str): raise TypeError("nextpiece must be in str")
        elif nextpiece.upper() not in ['O','X']: raise TypeError("nextpiece must be either 'O' or 'X'")
        return self.__calculate(nextpiece.upper())