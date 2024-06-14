from ..edgework import edgework

class caesarcipher(edgework):
    def __check(self, l):
        if not isinstance(l,list) and not isinstance(l,str): raise TypeError("letters must be in list or str")
        elif len(l)!=5: raise IndexError("Length of letters must be 5")
        elif not all([isinstance(a, str) for a in l]): raise TypeError("Element of letters must be in str")
        return [a.upper() for a in l]
    
    def __init__(self, edgework:edgework, letters:list|str):
        '''
        Initialize a new caesarcipher instance

        Args:
            edgework (edgework): The edgework of the bomb
            letters (list (str)|str): The letters that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__letters = self.__check(letters)
    
    def __calculate(self):
        offset = (1*self.batt)+(-1 if any([a in ['A','I','U','E','O'] for a in self._snletter]) else 0)+(1 if int(self._sndigit[-1])%2==0 else 0)+(1 if 'CAR' in self._unlitind or 'CAR*' in self._litind else 0)
        offset = 0 if 'PARALLEL' in self._uniqueports and 'NSA' in self.ind or 'NSA*' in self.ind else offset
        ans = [chr(((int(ord(a)-65)+offset)%26)+65) if offset>=0 else chr(((int(ord(a)-65)+(26+offset))%26)+65) for a in self.__letters]
        return ans

    def solve(self):
        '''
        Solve the Caesar Cipher module

        Returns:
            tuple (str): The order of letter to press. Index 0 is the first, index 4 is the last
        '''
        return tuple(self.__calculate())