from ..edgework import edgework

class password(edgework):
    __bank = ["about","after","again","below","could","every","first","found","great","house","large","learn","never","other","place","plant","point","right","small","sound","spell","still","study","their","there","these","thing","think","three","water","where","which","world","would","write"]
    
    def __check(self, l):
        if not isinstance(l, list): raise TypeError("Letter has an invalid type")
        elif len(l)!=5: raise IndexError("Length of letter column must be 5")
        elif any([True if not isinstance(a,list) else False for a in l]): raise TypeError("Letter must be made out of lists")
        elif any([True if len(a) != 6 else False for a in l]): raise IndexError("Each columns must have 6 letters")
        elif any([True if any([True if not isinstance(b, str) else False for b in a]) else False for a in l]): raise TypeError("Each letter must be in string")
        elif any([True if any([True if len(b)!=1 else False for b in a]) else False for a in l]): raise IndexError("Each letter can only have 1")
        return l

    def __init__(self, edgework: edgework, letter:list):
        '''
        Initialize a password instance

        Args:
            edgework (edgework): The edgework of the bomb
            letter (List [List [str]]): The possible letters for all 5 columns. There are 5 list representing 1 column of the letters. Each column list has 6 possible letters
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.strikes)
        self.__letters = self.__check([[b.lower() for b in a] for a in letter])
    
    def __calculate(self):
       transposed = list(zip(*self.__letters))
       comb = [''.join(chars) for chars in transposed]
       for a in self.__bank:
        if all(any(char in col for col in comb) for char in a):
            return a

    def solve(self):
        '''
        Solve the Password module

        Returns:
            str: The valid word with the possible letters presented on the module
        '''
        return self.__calculate()
