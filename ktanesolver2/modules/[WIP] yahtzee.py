from ..edgework import edgework
from ..colordict import _colorcheck

class yahtzee(edgework):
    def __check(self, c, n):
        if not isinstance(c, list): raise TypeError("Color must be in list")
        elif not isinstance(n, list): raise TypeError("Number must be in list")
        elif len(c) >5: raise IndexError("Color length must be in range of 1-5")
        elif len(n) >5: raise IndexError("Number length must be in range of 1-5")
        elif not all(isinstance(a, str) for a in c): raise TypeError("Elements of color must be in str")
        elif not all(isinstance(a, int) for a in n): raise TypeError("Elements of number must be in int")
        elif not all(a>0 and a<7 for a in n): raise ValueError("Elements of number must be in range of 1-6")
        return sorted([(_colorcheck(a),b) for a,b in zip(c,n)], key=lambda x: x[0])
    
    def __init__(self, edgework:edgework, color:list|None=None, number:list|None=None, colnum:list|None=None, keep:list|None=None):
        '''
        Initialize a new yahtzee instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (list [str, ...]): The color list of the dice. It is by default None. CAUTION: The color list MUST BE in sync with the number list
            number (list [int, ...]): The number list of each dice. It is by default None. CAUTION: The number list MUST BE in sync with the color list
            colnum (list [tuple (str, int)]): The color and number list of each dice. Each element must be a tuple of a single die, containing the color and a number of one die. It is set to none by default. You can use this to avoid unsync of two lists form color and number parameters
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if color==None and number==None and (colnum != None):
            self.__dice = self.__check([a[0] for a in colnum if isinstance(a[0], str)], [a[1] for a in colnum if isinstance(a[1], int)])
        elif colnum==None and (color!=None and number != None):
            self.__dice = self.__check(color, number)
        else: raise TypeError("yahtzee.__init__() missing 1 or 2 required positional argument: 'color' and 'number' | 'colnum'")
        self.__keep = []
    
    def __dicepattern(self):
        patterns = {'ls': False, 'ss': [False,-1], '3': False, '4': False, 'p':False, '2p': False, 'fh': False}
        dn = sorted([a[1] for a in self.__dice]); paircount = 0
        if dn[1]==dn[0]+1 and dn[2]==dn[0]+2 and dn[3]==dn[0]+3 and dn[4]==dn[0]+4: patterns['ls'] = True
        for i in range(len(dn)-4):
            if dn[i+1]==dn[i]+1 and dn[i+2]==dn[i]+2 and dn[i+3]==dn[i]+3: patterns['ss'] = [True, 0 if i==1 else -1]
        for i in set(dn):
            if dn.count(i) == 3: patterns['3'] = True
            if dn.count(i) == 4: patterns['4'] = True
            if dn.count(i) == 2: 
                patterns['p'] = True
                paircount += 1
        if paircount==2: patterns['2p'] = True
        if len(set(dn)) == 2:
            if dn.count(set(dn)[0])==2 and dn.count(set(dn)[1])==3: patterns['fh']=True
            elif dn.count(set(dn)[0])==3 and dn.count(set(dn)[1])==2: patterns['fh']=True
        return patterns

    def __calculate(self):
        pass


    def solve(self):
        ans = self.__calculate()
        return tuple(sorted(self.__keep, key=lambda x: x[0]))