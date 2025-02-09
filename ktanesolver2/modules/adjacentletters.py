from ..edgework import edgework

class adjacentletters(edgework):
    __table = {
        'A': ['GJMOY','HKPRW'], 'N': ['PQRSV','AFGHL'], 
        'B': ['IKLRT','CDFYZ'], 'O': ['HJLUZ','IQSTX'],
        'C': ['BHIJW','DEMTU'], 'P': ['DMNOX','CFHKR'],
        'D': ['IKOPQ','CJTUW'], 'Q': ['CEOPV','BDIKN'],
        'E': ['ACGIJ','KSUWZ'], 'R': ['AEGSU','BNOXY'],
        'F': ['CERVY','AGJPQ'], 'S': ['ABEKQ','GMVYZ'],
        'G': ['ACFNS','HOQYZ'], 'T': ['GVXYZ','CJLSU'],
        'H': ['LRTUX','DKMPS'], 'U': ['FMVXZ','BILNY'],
        'I': ['DLOWZ','EFNUV'], 'V': ['DHMNW','AEJQX'],
        'J': ['BQTUW','EHIOS'], 'W': ['DFHMN','GLQRT'],
        'K': ['AFPXY','DIORZ'], 'X': ['BDFKW','AJNOV'],
        'L': ['GKPTZ','ABRVX'], 'Y': ['BCHSU','EGMTW'],
        'M': ['EILQT','BFPWX'], 'Z': ['JNRSY','CLMPV']
    }
    
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g)!=3: raise IndexError("Length of grid must be 3")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==4 for a in g]): raise IndexError("Length of grid's element must be 4")
        elif not all([isinstance(a, str) for b in g for a in b]): raise TypeError("Type of each grid sublists must be str")
        elif not all([len(a)==1 for b in g for a in b]): raise IndexError("Length of each letter must be only 1")
        return [[b.upper() for b in a] for a in g]
    
    def __init__(self, edgework:edgework, grid=list[list[str]]):
        '''
        Initialize a new adjacentletters instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list (str)): The letter grids that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)
    
    def __calculate(self):
        ans = []
        for a in range(0,3):
            for b in range(0,4):
                if self.__grid[a-1][b] in self.__table[self.__grid[a][b]][1] if a-1>-1 else False: ans.append(tuple([a,b,self.__grid[a][b]]))
                elif self.__grid[a+1][b] in self.__table[self.__grid[a][b]][1] if a+1<3 else False: ans.append(tuple([a,b,self.__grid[a][b]]))
                elif self.__grid[a][b-1] in self.__table[self.__grid[a][b]][0] if b-1>-1 else False: ans.append(tuple([a,b,self.__grid[a][b]]))
                elif self.__grid[a][b+1] in self.__table[self.__grid[a][b]][0] if b+1<3 else False: ans.append(tuple([a,b,self.__grid[a][b]]))
        return tuple(ans)

    def solve(self):
        '''
        Solve the Adjacent Letters module

        Returns:
            tuple (tuple (int, int, str)): The coordinates of button that need to be pressed down before submitting. In sub-tuples, index 0 represents the row index 1 represents the column and index 2 is the letter of that button in that coordination
        '''
        return self.__calculate()