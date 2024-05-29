from ..edgework import edgework

class bitwiseoperations(edgework):
    __strtofunc = {
        'AND': lambda x,y: int(x,2)&int(y,2),
        'OR': lambda x,y: int(x,2)|int(y,2),
        'XOR': lambda x,y: int(x,2)^int(y,2),
        'NOT': lambda x,y: int(''.join([str(int(not int(a))) for a in x]), 2)
    }
    
    def __check(self, o, m):
        if not isinstance(o, str): raise TypeError("Operator must be in str")
        elif not isinstance(m, int): raise TypeError("Starting minutes must be in int")
        elif o not in ['AND', 'OR', 'XOR', 'NOT']: raise ValueError("This operator is not available in the module")
        elif m<0: raise ValueError("Starting minutes cannot be a negative integer")
        return self.__strtofunc[o], m

    def __init__(self, edgework:edgework, operator:str, starting_minutes:int):
        '''
        Initialize a new bitwiseoperations instance

        Args:
            operator (str): The operator that appears on the module
            starting_minutes (int): The starting minute of the bomb
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__operator, self.__startminute = self.__check(operator.upper(), starting_minutes)
    
    def __calculate(self):
        bin1 = []; bin2 = []
        bin1.append(self.batt-self.hold == 0); bin2.append(self.batt-((self.batt-self.hold)*2)>= 1)
        bin1.append('PARALLEL' in self._uniqueports); bin2.append(len([a for b in self.ports for a in b])>=3)
        bin1.append('NSA*' in self._litind); bin2.append(self.hold >= 2)
        bin1.append(self.total_modules > self.__startminute); bin2.append('BOB*' in self._litind)
        bin1.append(len(self._litind)>1); bin2.append(len(self._unlitind)>1)
        bin1.append(self.total_modules%3==0); bin2.append(int(self._sndigit[-1])%2==1)
        bin1.append(self.batt-((self.batt-self.hold)*2)<2); bin2.append(self.total_modules%2==0)
        bin1.append(len([a for b in self.ports for a in b])<4); bin2.append(self.batt>=2)
        bin1 = ''.join(list(map(lambda x: '1' if x else '0', bin1))); bin2 = ''.join(list(map(lambda x: '1' if x else '0', bin2)))
        print(bin1, bin2)
        return bin(self.__operator(bin1, bin2))[2:]


    def solve(self):
        '''
        Solve the Bitwise Operations module

        Returns:
            str: The binary to be submitted where index 0 is the leftmost column
        '''
        return self.__calculate()