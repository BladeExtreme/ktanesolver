from ..edgework import edgework

class emojimath(edgework):
    __table = {
        ':)': 0,
        '=(': 1,
        '(:': 2,
        ')=': 3,
        ':(': 4,
        '):': 5,
        '=)': 6,
        '(=': 7,
        ':|': 8,
        '|:': 9
    }

    def __check(self, d):
        if not isinstance(d, (str, list)): raise TypeError("display must be in str or list")
        if isinstance(d, str):
            if len(d)!=9: raise IndexError("Length of display must be 9 characters. 4 emojis with each emoji made out of 2 characters, and an operation. Make sure to have no spaces")
            a = 0; disp = []
            while a!=len(d):
                if d[a] in '+-':
                    disp.append(d[a])
                    a += 1
                else:
                    disp.append(d[a:a+2])
                    a += 2
            return disp
        elif isinstance(d, list):
            if not all([isinstance(a, str) for a in d]): raise TypeError("Element of display must be in str")
            elif len(d)!=5: raise IndexError("Length of display must be 5 items")
            elif not all([a in self.__table.keys() for a in d[0:2]+d[3:] if a not in '+-']): raise ValueError("Element of display must be emojis :), =(, (:, )=, :(, ):, =), (=, :|, |:")
            elif d[2] not in '+-': raise ValueError("Element of display must be an operation")
            return d
    
    def __init__(self, edgework:edgework, display:str|list[str]):
        '''
        Initializes a new emojimath instance

        Args:
            edgework (edgework): The edgework of the bomb
            display (str | list [str]): The display that appears on the module. Could be a full str, or a list of str (emojis and operation)
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__display = self.__check(display)
    
    def __calculate(self):
        n1 = self.__table[self.__display[0]]*10 + self.__table[self.__display[1]]; n2 = self.__table[self.__display[3]]*10 + self.__table[self.__display[4]]
        op = lambda x,y: x+y if self.__display[2]=='+' else x-y
        return op(n1, n2)

    def solve(self) -> int:
        '''
        Solve the Emoji Math module

        Returns:
            int: The correct answer to solve the module
        '''
        return self.__calculate()