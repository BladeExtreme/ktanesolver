from ..edgework import edgework
from ..tools.morsedict import _translate, _reverseTranslate

class morsematics(edgework):
    def __check(self, m):
        if not isinstance(m, tuple): raise TypeError("morse must be in tuple")
        elif len(m)!=3: raise IndexError("Length of morse must be 3")
        elif not all([isinstance(a, str) for a in m]): raise TypeError("Elements of morse must be in str")
        return [ord(_translate(a.lower()))-ord('A')+1 for a in m]

    def __init__(self, edgework:edgework, morse:tuple[str]):
        '''
        Initialize a morsematics instance

        Args:
            edgework (edgework): The edgework of the bomb
            morse (tuple [str]): The morse codes that appears on the module. First index is the first morse code to appear (leftmost), second index is the second morse and so on
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__morse = self.__check(morse)
    
    def __calculate(self):
        squares = [1,4,9,16,25,36,49]
        prime = [2,3,5,7,11,13,17,19,23]
        
        a = self.sn[3]; b = self.sn[4]
        if a.isalpha(): a = (ord(a)-ord('A'))+1
        else: a = int(a)
        if b.isalpha(): b = (ord(b)-ord('A'))+1
        else: b = int(b)
        
        for a in self.__morse:
            for b in self.ind:
                if a in b and '*' in b: a = (a+1)-26 if (a+1)>26 else a+1
                elif a in b and '*' not in b: b = (b+1)-26 if (b+1)>26 else b+1
        
        if a+b in squares: a = (a+4)-26 if (a+4)>26 else a+4
        else: b = (b+4)-26 if (b+4)>26 else b+4
        a = (max(self.__morse)+a)-26 if (max(self.__morse)+a)>26 else max(self.__morse)+a

        for z in self.__morse:
            if z in prime: a-=z
            if z in squares: b-=z
            if z%self.batt==0: a-=z; b-=z

            if a<0: a+=26
            if b<0: b+=26

        if a==b: return _reverseTranslate(chr(a+ord('A')-1))
        elif a>b: return _reverseTranslate(chr(a-b+ord('A')-1) if a-b>0 else chr((a-b)+ord('A')-1+26))
        elif a<b: return _reverseTranslate(chr(a+b+ord('A')-1) if a+b<=26 else chr((a+b)+ord('A')-1-26))

    def solve(self, character:bool|None=False) -> str:
        '''
        Solve the Morsematics module

        Args:
            character (bool): State if the result should be character or not

        Returns:
            str: The correct morse string to be submitted
        '''
        if not isinstance(character, bool): raise TypeError("character must be in bool")
        if character:
            return _translate(self.__calculate()).upper()
        else:
            return self.__calculate()