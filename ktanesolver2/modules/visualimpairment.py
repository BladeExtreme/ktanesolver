from ..edgework import edgework
from ..tools.colordict import _colorcheck

class visualimpairment(edgework):
    def __check(self, g, c):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif not isinstance(c, str): raise TypeError("grid must be in str")
        elif len(g)!=5: raise IndexError("Length of grid must be 5")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==5 for a in g]): raise IndexError("Length of grid's elements must be 5")
        elif not all([all([isinstance(b, int) for b in a]) for a in g]): raise TypeError("Each element of grid must be in int, representing a certain group color")
        return g, _colorcheck(c)

    def __init__(self, edgework:edgework, grid:list, color:str):
        '''
        Initialize a new visualimpairment instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list [list, ...]): The gray-scaled image that appears on the module. Each variation of gray color should be interpreted using any number of your choice but must be consistent, otherwise the grid will not be found or the answer may/may not match up
            color (str): The color of the squares that need to be pressed
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid, self.__color = self.__check(grid, color)
    
    def __rotate(self, l, n):
        return list([list(a) for a in zip(*l[::-n])])
    
    def __conversion(self, l):
        convertedgrid = []
        for a in range(1, len(l)):
            convertedgrid.append([(1 if l[a][b-1]!=l[a][b] else 0)+(1 if l[a-1][b]!=l[a][b] else 0) for b in range(1, len(l[a]))])
        return convertedgrid

    def __calculate(self):
        grids = [
            [
                ['r','g','r','w','g'],
                ['b','w','b','r','r'],
                ['g','b','r','b','g'],
                ['b','w','w','g','b'],
                ['r','b','w','g','r']
            ],[
                ['g','b','r','b','r'],
                ['g','g','g','r','w'],
                ['w','w','w','w','w'],
                ['w','r','g','g','g'],
                ['r','b','r','b','g']
            ],[
                ['b','b','b','r','r'],
                ['r','b','g','r','r'],
                ['r','g','g','g','b'],
                ['r','w','w','w','b'],
                ['r','b','w','b','b']
            ],[
                ['b','r','w','w','b'],
                ['w','r','b','r','b'],
                ['w','b','r','w','r'],
                ['g','w','b','w','g'],
                ['b','g','g','g','b']
            ],[
                ['r','g','r','g','w'],
                ['w','b','r','r','b'],
                ['b','b','r','w','w'],
                ['w','g','g','w','b'],
                ['b','r','g','r','g']
            ],[
                ['w','g','w','b','g'],
                ['b','g','r','b','w'],
                ['b','g','r','g','w'],
                ['r','w','b','g','b'],
                ['r','w','r','r','b']
            ],[
                ['g','r','w','r','w'],
                ['r','w','r','w','b'],
                ['b','r','w','b','g'],
                ['w','g','b','g','b'],
                ['r','w','g','b','g']
            ],[
                ['b','b','r','w','w'],
                ['b','g','w','g','w'],
                ['r','r','g','w','r'],
                ['b','g','g','g','r'],
                ['r','g','w','g','b']
            ],[
                ['w','b','r','w','g'],
                ['b','g','w','g','w'],
                ['r','w','b','w','r'],
                ['g','b','g','g','b'],
                ['w','r','g','r','b']
            ]
        ]
        
        mygrids = []
        for a in range(2):
            if a==0:
                currgrid = self.__grid; mygrids.append(currgrid)
                for b in range(1,4):
                    currgrid = self.__rotate(currgrid, 1)
                    mygrids.append(currgrid)
            elif a==1:
                currgrid = [a[::-1] for a in self.__grid]; mygrids.append(currgrid)
                for b in range(1,4):
                    currgrid = self.__rotate(currgrid, 1)
                    mygrids.append(currgrid)
        convertedgrid = []
        for a in range(len(mygrids)):
            convertedgrid.append(self.__conversion(mygrids[a]))
        
        converteddefaultgrid = []
        for a in range(len(grids)):
            converteddefaultgrid.append(self.__conversion(grids[a]))

        ans = []; ansgrid = []
        for a in range(len(converteddefaultgrid)):
            if converteddefaultgrid[a] in convertedgrid:
                ans = [convertedgrid.index(converteddefaultgrid[a]), a]
                ansgrid = [mygrids[ans[0]], grids[ans[1]]]
                break
        
        if len(ans)==0:
            raise ValueError("This pattern cannot be found")

        grouping = {'r': None, 'b': None, 'g': None, 'w': None}
        for a in range(len(ansgrid[0])):
            for b in range(len(ansgrid[0][a])):
                grouping[ansgrid[1][a][b]] = ansgrid[0][a][b]
        
        return grouping

    def solve(self):
        '''
        Solve the Visual Impairment module

        Returns:
            tuple (int, tuple): Index 0 is the number of the target color group that was represented on the gray-scaled color group. Index 1 are the squares that needed to be pressed. Each element represents the row and column of the square starting from 0.
        '''
        dictans = self.__calculate(); ans = []
        for a in range(len(self.__grid)):
            for b in range(len(self.__grid[a])):
                if dictans[self.__color[0]]==self.__grid[a][b]:
                    ans.append(tuple([a,b]))
        return tuple([dictans[self.__color[0]], tuple(ans)])