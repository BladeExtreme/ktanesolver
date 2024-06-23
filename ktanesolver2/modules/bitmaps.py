from ..edgework import edgework

class bitmaps(edgework):
    def __check(self, g,t,a):
        if not isinstance(g, list): raise TypeError("blackgridtotal must be in list")
        elif not isinstance(t, bool): raise TypeError("threebythree must be in bool")
        elif not isinstance(a, bool): raise TypeError("allcolrow must be in bool")
        elif not all([isinstance(a, int) for a in g]): raise TypeError("Element of blackgridtotal must be in int")
        elif not all([a in range(17) for a in g]): raise TypeError("Value of blackgridtotal must be in range 0-16")
        arr = []
        for x in g:
            temp = {'black': x, 'white': 16-x}
            arr.append(temp)
        return arr, t, a
    
    def __check2(self, x,arg):
        if not isinstance(x, int): raise TypeError(f"{arg} must be in int")
        elif x not in range(8): raise ValueError(f"coordinate of {arg} must be in range of 0-7")
        return x
    
    def __init__(self, edgework:edgework, blackgridtotal:list[int], threebythree:bool|None=False, allcolrow:bool|None=False, threebythreecoord:int|None=None, allcolrowcoord:int|None=None):
        '''
        Initialize a new bitmaps instance

        Args:
            edgework (edgework): The edgework of the bomb
            blackgridtotal (list [int]): The total amount of black grids in one quadrant.
            threebythree (bool|None): State if there are any 3x3 grid of all black/white in the module. By default it's False
            allcolrow (bool|None): State if there are any one row/column of all black/white in the module. By default it's False
            threebythreecoord (int|None): The x coordinate of the first square in top left. This must be int, if threebythree is True. By default it's None
            allcolrowcoord (int|None): The x coordinate of a column or y coordinate of a row. This must be int, if allcolrow is True. By default it's None
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if threebythree and threebythreecoord is None: raise TypeError("If threebythree is true, threebythreecoord cannot be None")
        if allcolrow and allcolrowcoord is None: raise TypeError("If allcolrow is true, allcolrowcoord cannot be None")
        if threebythree: self.__uniqsq = self.__check2(threebythreecoord)
        if allcolrow: self.__uniqline = self.__check2(allcolrowcoord)
        self.__gridtotal, self.__3x3, self.__all = self.__check(blackgridtotal, threebythree, allcolrow)
    
    def __calculate(self):
        rule = int(self._sndigit[-1])
        while 1:
            if rule==0 and [a['white']<=5 for a in self.__gridtotal].count(True)==1: return sum([a['white'] for a in self.__gridtotal if a['white']>5])%4
            elif rule==1 and len([a for a in self.__gridtotal if a['white']>a['black']])==len(self._litind): return self.batt%4
            elif rule==2 and self.__all: return self.__uniqline%4
            elif rule==3 and len([a for a in self.__gridtotal if a['black']>a['white']])>len([a for a in self.__gridtotal if a['white']>a['black']]): return len([a for a in self.__gridtotal if a['black']>a['white']])%4
            elif rule==4 and sum([a['white'] for a in self.__gridtotal])>=36: return sum([a['white'] for a in self.__gridtotal])%4
            elif rule==5 and len([a for a in self.__gridtotal if a['white']>a['black']])>len([a for a in self.__gridtotal if a['black']>a['white']]): return min([a['black'] for a in self.__gridtotal])%4
            elif rule==6 and [a['black']<=5 for a in self.__gridtotal].count(True)==1: return sum([a['black'] for a in self.__gridtotal if a['black']>5])%4
            elif rule==7 and len([a for a in self.__gridtotal if a['black']>a['white']])==len(self._unlitind): return len([a for b in self.ports for a in b])%4
            elif rule==8 and self.__3x3: return self.__uniqsq%4
            elif rule==9 and len([a for a in self.__gridtotal if a['black']>a['white']])==len([a for a in self.__gridtotal if a['white']>a['black']]): return int(self._sndigit[0])%4
            rule = (rule+1)%10
    
    def solve(self):
        '''
        Solve the Bitmaps module

        Returns:
            int: The correct number to press
        '''
        ans = self.__calculate()
        if ans==0: ans=4
        return ans