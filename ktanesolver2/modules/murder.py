from ..edgework import edgework

class murder(edgework):
    __suspectlist = ['miss scarlett', 'professor plum', 'mrs peacock', 'reverend green', 'colonel mustard', 'mrs white']
    __weaponlist = ['candlestick', 'dagger', 'lead pipe', 'revolver', 'rope', 'spanner']
    __locattable = [
        ['dining room', 'library', 'lounge', 'kitchen', 'study', 'conservatory'],
        ['study', 'hall', 'billiard room', 'lounge', 'kitchen', 'library'],
        ['kitchen', 'billiard room', 'ballroom', 'library', 'conservatory', 'dining room'],
        ['lounge', 'ballroom', 'dining room', 'conservatory', 'hall', 'kitchen'],
        ['billiard room', 'kitchen', 'study', 'ballroom', 'dining room', 'hall'],
        ['conservatory', 'lounge', 'library', 'study', 'billiard room', 'ballroom'],
        ['ballroom', 'conservatory', 'kitchen', 'hall', 'library', 'study'],
        ['hall', 'study', 'conservatory', 'dining room', 'lounge', 'billiard room'],
        ['library', 'dining room', 'hall', 'billiard room', 'ballroom', 'lounge']
    ]
    def __check(self,s,w,l):
        if not isinstance(s, list): raise TypeError("suspects must be in list")
        elif not isinstance(w, list): raise TypeError("weapons must be in list")
        elif not isinstance(l, str): raise TypeError("location must be in str")
        elif len(s)!=4: raise IndexError("Length of suspects must be 4")
        elif len(w)!=4: raise IndexError("Length of weapons must be 4")
        elif not all([isinstance(a, str) for a in s]): raise TypeError("Element of suspects must be in str")
        elif not all([isinstance(a, str) for a in w]): raise TypeError("Element of weapons must be in str")
        return [a.replace(".","").lower() for a in s], [a.lower() for a in w], l.lower()
    
    def __init__(self, edgework:edgework, suspects:list[str], weapons:list[str], location:str):
        '''
        Initialize a new murder instance

        Args:
            edgework (edgework): The edgework of the bomb
            suspects (list (str)): The list of suspects
            weapons (list (str)): The list of weapons
            location (str): The red marked location from the lists of all possible locations
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__suspects, self.__weapons, self.__location = self.__check(suspects, weapons, location)
    
    def __calculate(self):
        if 'TRN*' in self._litind: suspectrow = 4
        elif self.__location == 'dining room': suspectrow = 6
        elif [a for b in self.ports for a in b].count("STEREO RCA") >= 2: suspectrow = 7
        elif self.hold*2 == self.batt: suspectrow = 1
        elif self.__location == 'study': suspectrow = 3
        elif self.batt >= 5: suspectrow = 8
        elif 'FRQ' in self._unlitind : suspectrow = 0
        elif self.__location == 'conservatory': suspectrow=2
        else: suspectrow = 5

        if self.__location == 'lounge': weaponrow = 2
        elif self.batt >= 5: weaponrow = 0
        elif 'SERIAL' in self._uniqueports: weaponrow = 8
        elif self.__location == 'billiard room': weaponrow = 3
        elif self.batt == 0: weaponrow = 5
        elif len(self._litind) == 0: weaponrow = 4
        elif self.__location == 'hall': weaponrow = 6
        elif [a for b in self.ports for a in b].count('STEREO RCA') >= 2: weaponrow = 1
        else: weaponrow = 7

        suspectindex = [self.__suspectlist.index(b) for b in self.__suspects]; suspecttable = [self.__locattable[suspectrow][a] for a in range(len(self.__locattable[suspectrow])) if a in suspectindex]
        weaponindex = [self.__weaponlist.index(b) for b in self.__weapons]; weapontable = [self.__locattable[weaponrow][a] for a in range(len(self.__locattable[weaponrow])) if a in weaponindex]
        
        actuallocation = list(set(weapontable).intersection(set(suspecttable)))[0]
        return tuple([self.__suspectlist[self.__locattable[suspectrow].index(actuallocation)], self.__weaponlist[self.__locattable[weaponrow].index(actuallocation)], actuallocation])

    def solve(self):
        '''
        Solve the Murder module

        Returns:
            tuple (str): The correct suspect, weapon and the location of the actual murder
        '''
        return self.__calculate()