from ..edgework import edgework

class logic(edgework):
    def __check(self, t,b):
        if not callable(t): raise TypeError("toplogic must be callable/function")
        elif not callable(b): raise TypeError("bottomlogic must be callable/function")
        elif not all([len(a)==1 and a.isalpha() and a.islower() for a in t.__code__.co_varnames]): raise ValueError("Parameter of top logic must be a letter from alphabet and lowercase")
        elif not all([len(a)==1 and a.isalpha() and a.islower() for a in b.__code__.co_varnames]): raise ValueError("Parameter of bottom logic must be a letter from alphabet and lowercase")
        return t,b
    
    def __init__(self, edgework:edgework, toplogic:callable, bottomlogic:callable):
        '''
        Initialize a new logic instance

        Args:
            edgework (edgework): The edgework of the bomb
            toplogic (function): The top logic operation. Parameter's name are the letters that appears on the module
            bottomlogic (function): The bottom logic operation. Parameter's name are the letters that appears on the module
        NOTE:
            If you're confused how to translate the logical symbol to python here's a guide:\n
            x ∧ y = x and y\n
            x v y = x or y\n
            x ⊻ y = x ^ y\n
            x → y = not x or y\n
            x ← y = x or not y\n
            x | y = not (x and y)\n
            x ↓ y = not (x or y)\n
            x ↔ y = not (x ^ y)\n
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__toplogic, self.__bottomlogic = self.__check(toplogic, bottomlogic)
    
    def __calculate(self):
        statement = {
            'a': self.batt==len(self.ind), 'n': self.hold>2,
            'b': len(self._snletter)>len(self._sndigit), 'o': len(self._litind)>0 and len(self._unlitind)>0,
            'c': 'IND' in self._unlitind or 'IND*' in self._litind, 'p': 'PARALLEL' in self._uniqueports,
            'd': 'FRK' in self._unlitind or 'FRK*' in self._litind, 'q': len([a for b in self.ports for a in b])==2,
            'e': len(self._unlitind)==1, 'r': 'PS/2' in self._uniqueports,
            'f': len(self._uniqueports)>1, 's': sum([int(a) for a in self._sndigit])>10,
            'g': self.batt>2, 't': 'MSA' in self._unlitind or 'MSA*' in self._litind,
            'h': self.batt<2, 'u': self.hold==1,
            'i': int(self._sndigit[-1])%2==1, 'v': all([a not in "AIUEO" for a in self._snletter]),
            'j': self.batt>4, 'w': len(self.ind)==0,
            'k': len(self._litind)==1, 'x': len(self.ind)==1,
            'l': len(self.ind)==2, 'y': len([a for b in self.ports for a in b])>5,
            'm': [a for b in self.ports for a in b]==set([a for b in self.ports for a in b]), 'z': len([a for b in self.ports for a in b])<2
        }
        vartop = [statement[a] for a in self.__toplogic.__code__.co_varnames]; varbot = [statement[a] for a in self.__bottomlogic.__code__.co_varnames]; ans = {}
        ans['top'] = self.__toplogic(**dict(zip([a for a in self.__toplogic.__code__.co_varnames], vartop)))
        ans['bottom'] = self.__bottomlogic(**dict(zip([a for a in self.__bottomlogic.__code__.co_varnames], varbot)))
        return ans

    def solve(self):
        '''
        Solve the Logic module

        Returns:
            dict (str, bool): The answer to top or bottom logic operation. Keys of this dict are: 'top' and 'bottom'. Values of it are the result of the logic operation
        '''
        return self.__calculate()