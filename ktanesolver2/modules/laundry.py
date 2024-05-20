from ..edgework import edgework

class laundry(edgework):
    __item = {
        0: ['300°F', 'bleach'],
        1: ['no steam', 'no tetrachlorethylene'],
        2: ['iron', 'reduced moisture'],
        3: ['200°C', 'reduced moisture'],
        4: ['300°F', 'dont bleach'],
        5: ['110°C', 'dont dryclean']
    }

    __material = {
        0: ['50°', 'petroleum only'],
        1: ['95°', 'dont dryclean'],
        2: ['handwash', 'reduced moisture'],
        3: ['30°', 'low heat'],
        4: ['40°', 'wet cleaning'],
        5: ['30°', 'no tetrachlore']
    }

    __color = {
        0: ['3 dots', 'any solvent'],
        1: ['3 dots', 'low heat'],
        2: ['empty', 'short cycle'],
        3: ['crossed', 'no steam finish'],
        4: ['1 dot', 'no chlorine'],
        5: ['2 dots', 'no chlorine']
    }
    
    __letmat = ['polyester', 'cotton', 'wool', 'nylon', 'corduroy', 'leather']

    def __check(self, s):
        if not isinstance(s, int): raise TypeError("Solved has an invalid type")
        elif s<0: raise ValueError("Solved cannot be below 0")
        return s
    
    def __init__(self, edgework:edgework, solved: int):
        '''
        Initialize a new laundry instance

        Args:
            edgework (edgework): The edgework of the bomb
            solved (int): The total module solved
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.strikes)
        self.__solved = self.__check(solved)
    
    def __calculate(self):
        w = ''; d=''; ir=''
        i = ((self.total_modules - self.__solved) + len(self.ind))%6
        m = (len([a for b in self.ports for a in b]) + self.__solved - self.hold)%6
        c = (int(self._sndigit[-1])+self.batt)%6
        sp = -1

        if c == 4: sp = 'nochlorine'
        elif i == 0 or m==4: sp = self.__material[m][-1]
        elif any([a in set(self.__letmat[m].upper()) for a in self._snletter]): sp = self.__color[c][-1]
        else: sp = self.__item[i][-1]

        if c==3: w = '30°'
        if m==2: d = '3 dots'
        
        if ir=='': ir=self.__item[i][0]
        if w=='': w=self.__material[m][0]
        if d=='': d=self.__color[c][0]
        return w,d,ir,sp

    def solve(self):
        '''
        Solve the Laundry module

        Returns:
            tuple (str, str, str, str): Return the washing, drying, ironing, and special condition of laundry in that order
        '''
        if (self.batt == 4 and self.hold == 2 and 'BOB*' in self._litind): return 'unicorn'
        wash, drying, iron, special = self.__calculate()
        return tuple([wash, drying, iron, special])