from ..edgework import edgework

class fastmath(edgework):
    __table = [
        [25, 11, 53, 97, 2, 42, 51, 97, 12, 86, 55, 73, 33],
        [54, 7, 32, 19, 84, 33, 27, 78, 26, 46, 9, 13, 58],
        [86, 37, 44, 1, 5, 26, 93, 49, 18, 69, 23, 40, 22],
        [54, 28, 77, 93, 11, 0, 35, 61, 27, 48, 13, 72, 80],
        [99, 36, 23, 95, 67, 5, 26, 17, 44, 60, 26, 41, 67],
        [74, 95, 3, 4, 56, 23, 54, 29, 52, 38, 10, 76, 98],
        [88, 46, 37, 96, 2, 52, 81, 37, 12, 70, 14, 36, 78],
        [54, 43, 12, 65, 94, 3, 47, 23, 16, 62, 73, 46, 21],
        [7, 33, 26, 1, 67, 26, 27, 77, 83, 14, 27, 93, 9],
        [63, 64, 94, 27, 48, 84, 33, 10, 16, 74, 43, 99, 4],
        [35, 39, 3, 25, 47, 62, 38, 45, 88, 48, 34, 31, 27],
        [67, 30, 27, 71, 9, 11, 44, 37, 18, 40, 32, 15, 78],
        [13, 23, 26, 85, 92, 12, 73, 56, 81, 7, 75, 47, 99]
    ]
    __letindex = ['A','B','C','D','E','G','K','N','P','S','T','X','Z']
    
    def __init__(self, edgework:edgework):
        '''
        Initialize a new fastmath instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__offset = self.__calculate()
    
    def __calculate(self):
        offset = 0
        if 'MSA*' in self._litind: offset+=20
        if 'SERIAL' in self._uniqueports: offset+=14
        if any([a in ['F','A','S','T'] for a in self._snletter]): offset-=5
        if 'RJ-45' in self._uniqueports: offset+=27
        if self.batt>3: offset-=15
        return offset

    def __calculate1(self, n):
        number = (self.__table[self.__letindex.index(n[0])][self.__letindex.index(n[1])]+self.__offset)%100
        if number<0: number+=50
        return number

    def solve(self, letter:list|str):
        '''
        Solve the Fast Math module

        Args:
            letter (str): Two letters that appears on the module
        Returns:
            int: Result of the two letters after mathematic operations
        '''
        if not isinstance(letter, str) and not isinstance(letter, list): raise TypeError("letter must be in str or list")
        elif len(letter)!=2: raise IndexError("length of letter must be 2")
        elif not all([a.isalpha() for a in letter]): raise ValueError("letter must be made out of letters")
        return self.__calculate1([a.upper() for a in letter])