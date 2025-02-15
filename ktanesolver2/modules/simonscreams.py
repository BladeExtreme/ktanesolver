from ..edgework import edgework
from ..tools.colordict import _colorcheck

class simonscreams(edgework):
    def __check(self, c, s):
        if not isinstance(c, list): raise TypeError('color_list must be a list of strings')
        elif not isinstance(s, list): raise TypeError('sequence must be a list of strings')
        elif not all([isinstance(a, str) for a in c]): raise TypeError('Each element of color_list must be a string')
        elif not all([isinstance(a, str) for a in s]): raise TypeError('Each element of sequence must be a string')
        elif len(c) != 6: raise IndexError('color_list must have 6 elements')
        elif not all([_colorcheck(a.lower()) in ['red','orange','yellow','green','blue','purple'] for a in c]): raise ValueError('Each element of color_list must be in either [\'red\', \'orange\', \'yellow\', \'green\', \'blue\', \'purple\']')
        elif not all([_colorcheck(a.lower()) in ['red','orange','yellow','green','blue','purple'] for a in s]): raise ValueError('Each element of sequence must be in either [\'red\', \'orange\', \'yellow\', \'green\', \'blue\', \'purple\']')
        return [_colorcheck(a.lower()) for a in c], [_colorcheck(a.lower()) for a in s]

    def __check2(self, s):
        if not isinstance(s, list): raise TypeError('sequence must be a list of strings')
        elif not all([isinstance(a, str) for a in s]): raise TypeError('Each element of sequence must be a string')
        elif not all([_colorcheck(a.lower()) in ['red','orange','yellow','green','blue','purple'] for a in s]): raise ValueError('Each element of sequence must be in either [\'red\', \'orange\', \'yellow\', \'green\', \'blue\', \'purple\']')
        return [_colorcheck(a.lower()) for a in s]
    
    def __init__(self, edgework:edgework, color_list:list[str], sequence:list[str]):
        '''
        Initialize a new simonscreams instance

        Args:
            edgework (edgework): The edgework of the bomb
            color_list (list [str]): The color list starting from topmost one, then going clockwise. Index 0 is the topmost one, index 1 is clockwise from index 0, and so on
            sequence (list [str]): The color flashes sequence
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color_list, self.__sequence = self.__check(color_list, sequence)
        self.__seqNumber = 0
    
    def __checkrule(self):
        for a in range(len(self.__color_list)):
            if [self.__color_list[a], self.__color_list[(a+1)%6], self.__color_list[(a+2)%6]] in [[self.__sequence[b], self.__sequence[(b+1)%len(self.__sequence)], self.__sequence[(b+2)%len(self.__sequence)]] for b in range(len(self.__sequence)-2)]:
                return 0
        for a in range(len(self.__sequence)):
            if self.__sequence[a]==self.__sequence[(a+2)%len(self.__sequence)] and abs(self.__color_list.index(self.__sequence[(a+1)%len(self.__sequence)])-self.__color_list.index(self.__sequence[a]))==1: return 1
        if len([a for a in self.__sequence if a in ['red', 'yellow', 'blue']])<=1: return 2
        temp = sorted([self.__color_list.index(y) for y in list(set([a for a in self.__color_list if a not in self.__sequence]))])
        if len(temp)==2 and temp[0]+3==temp[1]: return 3
        for a in range(len(self.__color_list)):
            if [self.__color_list[a], self.__color_list[(a+1)%6]] in [[self.__sequence[b], self.__sequence[(b+1)%len(self.__sequence)]] for b in range(len(self.__sequence)-1)]:
                return 4
        return 5

    def __calculate(self):
        table = [
            ["FFC","CEH","HAF","ECD","DDE","AHA"],
            ["AHF","DFC","ECH","CDE","FEA","HAD"],
            ["DED","ECF","FHE","HAA","AFH","CDC"],
            ["HCE","ADA","CFD","DHH","EAC","FEF"],
            ["CAH","FHD","DDA","AEC","HCF","EFE"],
            ["EDA","HAE","AEC","FFF","CHD","DCH"]
        ]
        column_list = ['red','orange','yellow','green','blue','purple']
        color_column = {
            'A': ['yellow', 'purple', 'orange', 'green', 'red', 'blue'],
            'C': ['orange', 'yellow', 'green', 'blue', 'purple', 'red'],
            'D': ['green', 'red', 'blue', 'orange', 'yellow', 'purple'],
            'E': ['red', 'blue', 'purple', 'yellow', 'orange', 'green'],
            'F': ['blue', 'orange', 'red', 'purple', 'green', 'yellow'],
            'H': ['purple', 'green', 'yellow', 'red', 'blue', 'orange'],
        }
        color_row = []
        if len(self.ind)>=3: color_row.append(0)
        if len([a for b in self.ports for a in b]): color_row.append(1)
        if len(self._sndigit)>=3: color_row.append(2)
        if len(self._snletter)>=3: color_row.append(3)
        if self.batt>=3: color_row.append(4)
        if self.hold>=3: color_row.append(5)

        row = self.__checkrule()
        col = column_list.index(self.__sequence[self.__seqNumber])
        result = [color_column.get(table[row][col][self.__seqNumber])[a] for a in color_row]
        self.__seqNumber += 1
        return result


    def solve(self, append_sequence:list[str]|None=None, sequence:list[str]|None=None):
        '''
        Solve the Simon Screams module

        Args:
            append_sequence (list [str]|None): The new sequence to append to the original sequence. By default this value is None
            sequence (list [str]|None): The color flashes sequence. By default this value is None
        
        Returns:
            tuple (str): The color press in sequence where index 0 is the first color press
        '''
        if sequence is not None:
            self.__sequence = self.__check2(sequence)
        if append_sequence is not None:
            self.__sequence += self.__check2(append_sequence)
        return tuple(self.__calculate())