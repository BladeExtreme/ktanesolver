from ..edgework import edgework

class symbolicpassword(edgework):
    __nametable = [
    	['balloon', 'euro', 'copyright', 'six', 'pitchfork', 'six', 'questionmark'],
    	['at', 'balloon', 'pumpkin', 'paragraph', 'smileyface', 'euro', 'hollowstar'],
    	['upsidedowny', 'leftc', 'cursive', 'bt', 'bt', 'tracks', 'balloon'],
    	['squigglyn', 'cursive', 'doublek', 'squidknife', 'rightc', 'ae', 'upsidedowny'],
    	['squidknife', 'hollowstar', 'meltedthree', 'doublek', 'paragraph', 'pitchfork', 'cursive'],
    	['hookn', 'hookn', 'upsidedowny', 'questionmark', 'dragon', 'nwithhat', 'euro'],
    	['leftc', 'questionmark', 'hollowstar', 'smileyface', 'filledstar', 'omega', 'pumpkin']
    ]
    __namelist = ['balloon', 'euro', 'copyright', 'six', 'pitchfork', 'at', 'pumpkin', 'paragraph', 'smileyface', 'upsidedowny', 'leftc', 'cursive', 'bt', 'tracks', 'squigglyn', 'doublek', 'squidknife', 'rightc', 'ae', 'hollowstar', 'meltedthree', 'hookn', 'questionmark', 'dragon', 'nwithhat', 'reversedc', 'filledstar', 'omega']
    __symboltable = [
    	['Ϙ', 'Ӭ', '©', 'б', 'Ψ', 'б'],
    	['Ѧ', 'Ϙ', 'Ѽ', '¶', 'ټ', 'Ӭ'],
    	['ƛ', 'Ͽ', 'Ҩ', 'Ѣ', 'Ѣ', '҂'],
    	['Ϟ', 'Ҩ', 'Җ', 'Ѭ', 'Ͼ', 'æ'],
    	['Ѭ', '☆', 'Ԇ', 'Җ', '¶', 'Ψ'],
    	['ϗ', 'ϗ', 'ƛ', '¿', 'Ѯ', 'Ҋ'],
    	['Ͽ', '¿', '☆', 'ټ', '★', 'Ω']
    ]
    __symbollist = ['Ϙ', 'Ӭ', '©', 'б', 'Ψ', 'Ѧ', 'Ѽ', '¶', 'ټ', 'ƛ', 'Ͽ', 'Ҩ', 'Ѣ', '҂', 'Ϟ', 'Җ', 'Ѭ', 'Ͼ', 'æ', '☆', 'Ԇ', 'ϗ', '¿', 'Ѯ', 'Ҋ', '★', 'Ω']
    
    def __check(self, s):
        if not isinstance(s, list): raise TypeError("symbollist has an invalid type")
        elif len(s)!=6: raise IndexError("symbollist length must be 6")
        elif len(set([True if a in self.__namelist else False for a in s]))==2 and len(set([True if a in self.__symbollist else False for a in s]))==2: raise ValueError("List must be consistent. Either all symbols or all names")
        else: return s
    
    def __init__(self, edgework:edgework, symbollist:list):
        '''
        Initialize a new symbolicpassword instance

        Args:
            edgework (edgework): The edgework of the bomb
            symbollist (list (str)): The symbols or its name that appears on the module in no particular order
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__symbols = self.__check(symbollist)
    
    def __calculate(self, u):
        s = self.__symboltable if u==1 else self.__nametable
        for a in range(len(s)-1):
            for b in range(len(s[a])-2):
                if set(self.__symbols)==set([s[a][b], s[a][b+1], s[a][b+2], s[a+1][b], s[a+1][b+1], s[a+1][b+2]]):
                    return [s[a][b:b+3], s[a+1][b:b+3]]

    def solve(self):
        '''
        Solve the Symbolic Password module

        Returns:
            list (list (str), list (str)): The correct arrangement of the present symbols in that order. Index 0 are top row, index 1 are bottom row
        '''
        use = 0 if all([True if a in self.__namelist else False for a in self.__symbols]) else 1
        return self.__calculate(use)