from ..edgework import edgework

class keypad(edgework):
    __nametable = [
        ['balloon', 'at', 'upsidedowny', 'squigglyn', 'squidknife', 'hookn', 'reversedc'],
        ['euro', 'balloon', 'leftc', 'cursive', 'hollowstar', 'hookn', 'questionmark'],
        ['copyright', 'pumpkin', 'cursive', 'doublek', 'meltedthree', 'upsidedowny', 'hollowstar'],
        ['six', 'paragraph', 'bt', 'squidknife', 'doublek', 'questionmark', 'smileyface'],
        ['pitchfork', 'smileyface', 'bt', 'rightc', 'paragraph', 'dragon', 'filledstar'],
        ['six', 'euro', 'tracks', 'ae', 'pitchfork', 'nwithhat', 'omega']
    ]
    __namelist = ['balloon', 'euro', 'copyright', 'six', 'pitchfork', 'at', 'pumpkin', 'paragraph', 'smileyface', 'upsidedowny', 'leftc', 'cursive', 'bt', 'tracks', 'squigglyn', 'doublek', 'squidknife', 'rightc', 'ae', 'hollowstar', 'meltedthree', 'hookn', 'questionmark', 'dragon', 'nwithhat', 'reversedc', 'filledstar', 'omega']
    __symboltable = [
	    ['Ϙ', 'Ѧ', 'ƛ', 'Ϟ', 'Ѭ', 'ϗ', 'Ͽ'],
	    ['Ӭ', 'Ϙ', 'Ͽ', 'Ҩ', '☆', 'ϗ', '¿'],
	    ['©', 'Ѽ', 'Ҩ', 'Җ', 'Ԇ', 'ƛ', '☆'],
	    ['б', '¶', 'Ѣ', 'Ѭ', 'Җ', '¿', 'ټ'],
	    ['Ψ', 'ټ', 'Ѣ', 'Ͼ', '¶', 'Ѯ', '★'],
	    ['б', 'Ӭ', '҂', 'æ', 'Ψ', 'Ҋ', 'Ω']
    ]
    __symbollist = ['Ϙ', 'Ӭ', '©', 'б', 'Ψ', 'Ѧ', 'Ѽ', '¶', 'ټ', 'ƛ', 'Ͽ', 'Ҩ', 'Ѣ', '҂', 'Ϟ', 'Җ', 'Ѭ', 'Ͼ', 'æ', '☆', 'Ԇ', 'ϗ', '¿', 'Ѯ', 'Ҋ', '★', 'Ω']

    def __init__(self, edgework: edgework, symbols: list):
        '''
        Initialize a keypad instance

        Args:
            edgework (edgework): The edgework of the bomb
            symbols (list [str]): The symbols or name of the symbols that appears on the bomb
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__symbols = self.__check(symbols)
    
    def __check(self, s):
        if not isinstance(s, list): raise TypeError("Symbol has an invalid type")
        elif len(s)!=4: raise IndexError("List length must be 4")
        elif len(set([True if a in self.__namelist else False for a in s]))==2 and len(set([True if a in self.__symbollist else False for a in s]))==2: raise ValueError("List must be consistent. Either all symbols or all names")
        else: return s
    
    def __calculate(self, u):
        if u==1: s = self.__symboltable
        elif u==0: s = self.__nametable
        for a in s:
            if all([True if b in a else False for b in self.__symbols]): return a

    def solve(self):
        '''
        Solve the Keypad module

        Returns:
            Tuple (str): The correct order of presses
        '''
        use = 0 if all([True if a in self.__namelist else False for a in self.__symbols]) else 1
        row = self.__calculate(use)
        return tuple([a for a in row if a in self.__symbols])