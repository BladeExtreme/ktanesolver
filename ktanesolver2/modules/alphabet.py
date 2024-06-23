from ..edgework import edgework

class alphabet(edgework):
    __wordbank = ['JQXZ','QEW','AC','ZNY','TJL','OKBV','DFW','YKQ','LXE','GS','VSI','PQJS','VCN','JR','IRNM','OP','QYDX','HDU','PKD','ARGF']
    
    def __check(self, l):
        if not isinstance(l, list): raise TypeError("letters must be in list")
        elif len(l)!=4: raise IndexError("Length of letters must be 4")
        elif not all([isinstance(a, str) for a in l]): raise TypeError("Element of letters must be in str")
        elif not all([len(a)==1 for a in l]): raise TypeError("Element of letters must have a length of only 1")
        return [a.upper() for a in l]
    
    def __init__(self, edgework:edgework, letters:list[str]):
        '''
        Initialize a new alphabet instance

        Args:
            edgework (edgework): The edgework of the bomb
            letters (list [str]): List of letter in any order
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__letters = self.__check(letters)
    
    def __calculate(self):
        ans = []
        for a in self.__wordbank:
            if set([b for b in a])==set([b for b in a if b in self.__letters]):
                ans = [b for b in a]
                break
        if len(ans)!=4:
            for a in sorted(self.__letters):
                if a not in ans: ans.append(a)
        return ans
    
    def solve(self):
        '''
        Solve the Alphabet module

        Returns:
            tuple [str]: The order of letters to press. Index 0 is the first press
        '''
        return tuple(self.__calculate())