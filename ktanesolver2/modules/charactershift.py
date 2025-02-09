from ..edgework import edgework

class charactershift(edgework):
    def __check(self, l, n):
        if not isinstance(l, list): raise TypeError("letters must be in list")
        elif not isinstance(n, list): raise TypeError("numbers must be in list")
        elif not all([isinstance(a, str) for a in l]): raise TypeError("Element of letters must be in str")
        elif not all([isinstance(a, int) for a in n]): raise TypeError("Element of numbers must be in int")
        l = [a.upper() for a in l if a!='*']; n = [a for a in n if a!='*']
        return l,n
    
    def __init__(self, edgework, letters, numbers):
        '''
        Initialize a new charactershift instance

        Args:
            edgework (edgework): The edgework of the bomb
            letters (list (str)): The list of letters that appears on the module
            numbers (list (int)): The list of numbers that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__let, self.__num = self.__check(letters, numbers)
    
    def __operation(self, l, n, x, y):
        l = ord(l)-ord('A'); ans = 0
        func_op = {
            0: l+3,
            1: l+x,
            2: l-y,
            3: l+x-self._plates,
            4: l+int(self._sndigit[-1]),
            5: l-self.hold+(x*2),
            6: l+len(self._litind)+y-len(self._unlitind),
            7: l+(x if 'SIG*' in self._litind else y),
            8: l+x+y-len(self.ind)+abs((self.batt-self.hold)-self.hold),
            9: l+(x if self.batt>3 else -x)+(y if len(self.ind)>3 else -y)
        }
        ans = chr(func_op[n]%26 + ord('A'))
        return ans

    def __calculate(self):
        x = len([a for b in self.ports for a in b])+len(self._snletter)
        y = len(self.ind)+len(self._sndigit)
        valid_ans = []

        for a in self.__let:
            for b in self.__num:
                retchr = self.__operation(a, b, x, y)
                if retchr in self._snletter: valid_ans.append([a,b])
        return valid_ans

    def solve(self):
        '''
        Solve the Character Shift modulle

        Returns:
            list (list (str, int)): The possible answers to be submitted to the module. Index 0 represents the letter, index 1 represents the number to be submitted
        '''
        ans = self.__calculate()
        return ans