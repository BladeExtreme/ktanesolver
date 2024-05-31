from ..edgework import edgework
from ..colordict import _colorcheck

class simonstates(edgework):
    __prioritydict = {
        'red': ['red','blue','green','yellow'],
        'blue': ['blue','yellow','red','green'],
        'green': ['green','red','yellow','blue'],
        'blue': ['yellow','green','blue','red']
    }
    
    def __check(self, d, s):
        if not isinstance(d, str): raise TypeError("Dominant must be in str")
        elif not isinstance(s, list): raise TypeError("Sequence must be in list")
        elif not all([isinstance(a, str) or isinstance(a,list) for a in s]): raise TypeError("Element of sequence must be in str/list")
        elif not all([all([isinstance(b, str) for b in a] for a in s if isinstance(a, list))]): raise TypeError("List type element of sequence must contain str only")
        d = _colorcheck(d)
        for a in range(len(s)): s[a] = _colorcheck(s[a])
        return d,s
    
    def __init__(self, edgework:edgework, dominant:str, sequence:list, stage:int|None=None):
        '''
        Initialize a new simonstates instance

        Args:
            edgework (edgework): The edgework of the bomb
            dominant (str): The dominant color (top left) in the module
            sequence (list [str|list [str, ...], ...]): The color flashes sequence
            stage (int|None): The stage of simon states. By default it is set to None, and starts with stage 1 and increments by 1 for every call of simonstates.solve()
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__dominant, self.__sequence = self.__check(dominant.lower(), sequence)
        self.__priority = self.__prioritydict[self.__dominant]
        self.__anssequence = []
        self.__stage = 1 if stage==None else stage
        if stage!=None:
            for i in range(stage): self.__anssequence.append(None)
    
    def __calculate(self):
        length = len(self.__sequence) if isinstance(self.__sequence, list) else 1
        if self.__stage == 1:
            if length==1: return self.__sequence[-1]
            elif length==2: 
                if 'blue' in self.__sequence: return [a for a in self.__priority if a in self.__sequence][0]
                else: return 'blue'
            elif length==3:
                if 'red' in self.__sequence: return [a for a in self.__priority if a in self.__sequence][-1]
                else: return 'red'
            elif length==4:
                return self.__priority[1]
        elif self.__stage == 2:
            if length==1:
                if self.__sequence == 'blue': return 'yellow'
                else: return 'blue'
            elif length==2:
                if sorted(set(['blue', 'red'])) == self.__sequence: [a for a in self.__priority if a in ['green', 'yellow']][0]
                else: return [a for a in self.__priority if a not in self.__sequence][-1]
            elif length==3:
                return [a for a in self.__priority if a not in self.__sequence][0]
            elif length==4:
                return self.__anssequence[0]
        elif self.__stage == 3:
            if length==1: return self.__sequence[-1]
            elif length==2:
                if self.__sequence[0] in self.__anssequence and self.__sequence[1] in self.__anssequence: return [a for a in self.__priority if a not in self.__sequence][-1]
                else: return self.__sequence[-1]
            elif length==3:
                return [a for a in self.__priority if a in self.__sequence and a not in set(self.__anssequence)][0]
            elif length==4:
                return self.__priority[2]
        elif self.__stage == 4:
            if len(set(self.__anssequence))==3: return [a for a in self.__priority if a not in set(self.__anssequence)][0]
            elif length==1: return self.__sequence[-1]
            elif length==2: return 'green'
            elif length==3:
                if len(set(self.__sequence))-len([a for a in self.__anssequence if a in self.__sequence]) == 1: return [a for a in self.__anssequence if a not in self.__sequence][0]
                else: return self.__priority[-1]
            elif length==4:
                return self.__priority[-1]

    def solve(self, sequence:list|None=None):
        '''
        Solve the Simon States module

        Args:
            sequence (list [str|list [str, ...], ...]): The color flashes sequence. Used to skip new intialization
        Returns:
            Tuple (str, ...): The correct color presses where index 0 is the first press
        '''
        if sequence!=None: self.__dominant, self.__sequence = self.__check(self.__dominant, sequence)
        ans = self.__calculate()
        self.__anssequence.append(ans)
        self.__stage += 1 if self.__stage < 4 else -4
        return tuple(self.__anssequence)