from ..edgework import edgework
from ..tools.colordict import _colorcheck

class perspectivepegs(edgework):
    def __init__(self, edgework:edgework):
        '''
        Initialize a new perspectivepegs instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
    
    def __calculate(self):
        table = {
            0: 'red', 3: 'red',         5: 'blue', 8: 'blue',
            4: 'yellow', 9: 'yellow',   2: 'purple', 6: 'purple',
            1: 'green', 7: 'green'
        }
        diff = 0
        for a in range(0, len(self._snletter)-1, 2):
            diff += abs(int(ord(self._snletter[a])-64)-int(ord(self._snletter[a+1])-64))
        return table[diff%10]
    
    def __calculate1(self, s):
        table = [
            {
                tuple(['red','yellow','yellow']): ['blue','purple','yellow'],
                tuple(['yellow','purple','green']): ['purple','blue','red'],
                tuple(['red','green','purple']): ['blue','green','red'],
                tuple(['yellow','blue','green']): ['blue','yellow','yellow'],
                tuple(['purple','purple','red']): ['red','yellow','purple'],
                tuple(['blue','green','blue']): ['purple','yellow','green'],
                tuple(['yellow','green','blue']): ['green','purple','yellow'],
                tuple(['purple','green','green']): ['green','yellow','red']
            },{
                tuple(['blue','purple','blue']): ['yellow','blue','green'],
                tuple(['yellow','yellow','purple']): ['blue','red','purple'],
                tuple(['green','red','blue']): ['yellow','purple','blue'],
                tuple(['red','purple','yellow']): ['green','blue','green'],
                tuple(['yellow','green','green']): ['purple','blue','red'],
                tuple(['green','purple','blue']): ['yellow','green','yellow,'],
                tuple(['purple','red','purple']): ['blue','blue','green'],
                tuple(['red','yellow','red']): ['red','purple','blue'],
            },{
                tuple(['purple','yellow','blue']): ['red','green','blue'],
                tuple(['yellow','red','purple']): ['red','yellow','red'],
                tuple(['green','yellow','red']): ['green','blue','purple'],
                tuple(['blue','yellow','green']): ['purple','green','red'],
                tuple(['red','purple','yellow']): ['green','yellow','blue'],
                tuple(['purple','purple','green']): ['purple','blue','red'],
                tuple(['red','yellow','yellow']): ['blue','blue','red'],
                tuple(['yellow','green','purple']): ['purple','yellow','yellow']
            }
        ]
        tabletouse = 0 if self.batt in range(1,3) else 1 if self.batt in range(3,5) else 2
        for a in table[tabletouse]:
            for b in range(len(s)):
                if a == tuple([s[b], s[(b+1)%len(s)], s[(b+2)%len(s)]]):
                    temp = table[tabletouse][a]
                    s[b] = temp[0]; s[(b+1)%len(s)] = temp[1]; s[(b+2)%len(s)] = temp[2]
                elif a == tuple([s[(b+2)%len(s)], s[(b+1)%len(s)], s[b]]):
                    temp = table[tabletouse][a]
                    s[b] = temp[2]; s[(b+1)%len(s)] = temp[1]; s[(b+2)%len(s)] = temp[0]
        return s

    def solve(self, sequence:list|None=None):
        '''
        Solve the Perspective Pegs module

        Args:
            sequence (list (str)): The sequence of a color, starting from a peg whose majority color is the same as the key (return value without args)
        Returns:
            str: If sequence is None, returns the key color
            tuple (str, ...): The correct color sequence in this order
        '''
        if sequence is None:
            return self.__calculate()
        else:
            if not isinstance(sequence, list): raise TypeError("sequence must be in list")
            elif not all([isinstance(a, str) for a in sequence]): raise TypeError("Element of sequence must be in str")
            elif len(sequence)!=5: raise IndexError("Length of sequence must be 5")
            return tuple(self.__calculate1([_colorcheck(a.lower()) for a in sequence]))