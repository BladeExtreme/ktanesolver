from ..edgework import edgework

class textfield(edgework):
    __table = {
        'FB01':[
            ['D','C','F','A'],
            ['B','E','F','F'],
            ['B','B','B','C']
        ],
        'DC52':[
            ['C','B','D','E'],
            ['A','F','D','C'],
            ['B','E','B','D']
        ],
        '965A':[
            ['C','B','E','F'],
            ['E','B','F','E'],
            ['D','C','A','A']
        ],
        '7F67':[
            ['A','D','C','B'],
            ['A','C','B','C'],
            ['A','E','F','A']
        ],
        '1459':[
            ['B','A','B','B'],
            ['C','D','F','D'],
            ['D','F','C','E']
        ],
        'A0C1':[
            ['E','C','F','A'],
            ['C','F','B','D'],
            ['F','F','B','C']
        ],
        'BBFF':[
            ['D','A','B','F'],
            ['D','F','B','E'],
            ['C','E','B','A']
        ],
        'AA12':[
            ['B','E','A','B'],
            ['E','D','F','A'],
            ['B','C','E','C']
        ]
    }
    
    def __check(self, l):
        if not isinstance(l, str): raise TypeError("Letter must be in str")
        return l.upper()
    
    def __init__(self, edgework:edgework, letter:str):
        '''
        Initialize a textfield instance

        Args:
            edgework (edgework): The edgework of the bomb
            letter (str): The letter that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__letter = self.__check(letter)
    
    def __calculate(self):
        board = ''
        if self.__letter=='A':
            if 'CLR*' in self._litind: board = '1459'
            elif self.batt>2: board = 'BBFF'
            elif self.batt==1: board = '7F67'
            elif 'FRK*' in self._litind: board = 'DC52'
            else: board = 'A0C1'
        elif self.__letter=='B':
            if self.batt==0: board = '965A'
            elif int(self._sndigit[-1])%2==1: '1459'
            elif 'SERIAL' not in self._uniqueports: board = 'DC52'
            elif 'TRN*' in self._litind: board = 'A0C1'
            else: board = '7F67'
        elif self.__letter=='C':
            if 'DVI-D' in self._uniqueports: board = 'AA12'
            elif self.batt==2: board = 'FB01'
            elif all([a.upper() not in "AIUEO" for a in self._snletter]): board = 'DC52'
            elif 'CAR*' in self._litind: board = '1459'
            else: board = '7F67'
        elif self.__letter=='D':
            if 'PARALLEL' in self._uniqueports: board = 'FB01'
            elif self.batt<2: board = 'AA12'
            elif 'SIG*' in self._litind: board = 'BBFF'
            elif 'PS/2' not in self._uniqueports: board = '965A'
            else: board = '1459'
        elif self.__letter=='E':
            if self.batt<3: board = '7F67'
            elif 'STEREO RCA' not in self._uniqueports: board = 'AA12'
            elif 'BOB*' in self._litind: board = 'A0C1'
            elif 'RJ-45' in self._uniqueports: board = 'BBFF'
            else: board = 'DC52'
        elif self.__letter=='F':
            if 'SERIAL' not in self._uniqueports: board = 'DC52'
            elif any([a.upper() in "AIUEO" for a in self._snletter]): board = 'A0C1'
            elif 'IND*' in self._litind: board = '1459'
            elif int(self._sndigit[-1])%2==0: board = 'FB01'
            else: board = 'AA12'
        
        ans = []
        for a in range(len(self.__table[board])):
            if self.__letter in self.__table[board][a]: ans.append([self.__table[board][a].index(self.__letter), a])
        return tuple(ans)

    def solve(self) -> tuple[list[int]]:
        '''
        Solve the Text Field module

        Returns:
            tuple (int): The index of the correct letter to press from the given list. Each index is a list, where the first index of the list is the x coordinate and the second index is the y coordinate of the table
        '''
        return self.__calculate()