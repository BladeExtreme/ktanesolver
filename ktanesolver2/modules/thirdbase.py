from ..edgework import edgework

class thirdbase(edgework):
    __bank = [
        ['SZN6'],
        ['IH6X','I8O9','X6IS'],
        ['NHXS','H68S','6NZH','IS9H'],
        ['Z8IX','6O8I','NXO8','9NZS','ZHOX','SI9X','X9HI'],
        ['8OXN','66I8','S89H','HZN9'],
        ['XI8Z','XOHZ','SXHN','H6SI','SNZX','8I99','ZSN8','XZNS','8NSZ']
    ]
    __list = {
        'XI8Z': ['NHXS', 'I8O9', 'XOHZ', '6O8I', '6NZH', '66I8', 'H6SI', 'Z8IX', 'XI8Z'],
        'H68S': ['6NZH', 'I8O9', 'NHXS', '6O8I', 'SXHN', 'H6SI', 'IH6X', '8OXN', 'NXO8', 'XI8Z', 'Z8IX', 'XOHZ', '66I8', 'H68S'],
        'SXHN': ['Z8IX', '8OXN', 'NXO8', 'H68S', 'XOHZ', 'XI8Z', 'H6SI', 'NHXS', 'IH6X', '6NZH', '66I8', 'I8O9', 'SXHN'],
        'Z8IX': ['NXO8', 'H6SI', 'I8O9', '6O8I', 'Z8IX'],
        'IH6X': ['8OXN', 'H6SI', 'I8O9', '6O8I', 'NHXS', 'Z8IX', 'SXHN', '66I8', '6NZH', 'XOHZ', 'NXO8', 'H68S', 'IH6X'],
        'NHXS': ['I8O9', 'H6SI', '8OXN', '6O8I', 'H68S', 'XOHZ', '66I8', 'XI8Z', 'IH6X', 'NHXS'],
        'XOHZ': ['8OXN', 'XOHZ'],
        '8OXN': ['XI8Z', 'IH6X', '6NZH', 'XOHZ', 'I8O9', 'NHXS', 'H6SI', 'SXHN', '66I8', 'Z8IX', '8OXN'],
        '6NZH': ['H6SI', '6NZH'],
        'H6SI': ['NHXS', 'IH6X', 'XI8Z', '66I8', 'SXHN', 'NXO8', 'XOHZ', 'H6SI'],
        '6O8I': ['Z8IX', 'XI8Z', 'I8O9', 'XOHZ', 'IH6X', '66I8', 'SXHN', 'NXO8', '6NZH', '6O8I'],
        'I8O9': ['6O8I', 'SXHN', 'H68S', 'NHXS', '8OXN', 'IH6X', 'NXO8', 'I8O9'],
        'NXO8': ['8OXN', 'SXHN', 'Z8IX', 'I8O9', 'NHXS', '6NZH', 'H68S', '66I8', 'XOHZ', 'NXO8'],
        '66I8': ['H6SI', '6O8I', 'NHXS', 'XI8Z', '66I8'],
        '9NZS': ['8NSZ', '8I99', 'ZHOX', 'HZN9', 'IS9H', 'SNZX', 'SZN6', 'XZNS', 'SI9X', '9NZS'],
        '8I99': ['ZHOX', 'IS9H', 'X6IS', 'SNZX', 'SI9X', 'X9HI', 'ZSN8', 'XZNS', '9NZS', 'S89H', 'HZN9', '8NSZ', 'SZN6', '8I99'],
        'ZHOX': ['ZSN8', '8I99', 'SNZX', 'ZHOX'],
        'HZN9': ['9NZS', 'HZN9'],
        'SZN6': ['X9HI', 'S89H', 'SZN6'],
        'S89H': ['SNZX', '8NSZ', 'IS9H', 'SI9X', 'HZN9', 'SZN6', 'ZSN8', 'X9HI', 'S89H'],
        'SNZX': ['SNZX'],
        'ZSN8': ['SZN6', 'S89H', '8I99', 'HZN9', 'IS9H', 'ZSN8'],
        'SI9X': ['9NZS', 'XZNS', 'HZN9', 'ZHOX', 'S89H', 'X9HI', 'ZSN8', 'X6IS', '8I99', 'SNZX', 'SZN6', 'IS9H', 'SI9X'],
        'X9HI': ['8NSZ', 'SNZX', 'IS9H', 'SI9X', 'ZHOX', 'SZN6', 'HZN9', 'XZNS', 'X6IS', '9NZS', 'S89H', '8I99', 'ZSN8', 'X9HI'],
        'IS9H': ['SI9X', 'SNZX', 'ZSN8', 'ZHOX', 'XZNS', '8NSZ', 'IS9H'],
        'XZNS': ['8I99', 'S89H', 'X9HI', 'ZSN8', '9NZS', 'SZN6', '8NSZ', 'SI9X', 'HZN9', 'IS9H', 'XZNS'],
        '8NSZ': ['8I99', 'X9HI', 'X6IS', 'HZN9', '9NZS', 'XZNS', 'SNZX', 'SZN6', '8NSZ'],
        'X6IS': ['HZN9', 'IS9H', 'S89H', 'SZN6', 'XZNS', 'X9HI', 'ZSN8', 'SI9X', 'SNZX', '9NZS', 'X6IS']
    }
    
    def __reverse(self, t):
        reversebank = {'I': 'I', 'N': 'N', '9': '6', '6': '9', 'O':'O', 'S':'S', 'Z':'Z', 'X':'X', 'H': 'H', '8': '8'}
        return "".join([reversebank[a] for a in t][::-1])
    
    def __checkb(self, b, n):
        if not isinstance(b, list): raise TypeError("buttons must be in str" if n==0 else "reversedbuttons must be in str")
        elif len(b)!=6: raise IndexError(f"{'buttons' if n==0 else 'reversedbuttons'} must have a length of 6 elements")
        elif not all([isinstance(a, str) for a in b]): raise TypeError(f"Element of {'buttons' if n==0 else 'reversedbuttons'} must be in str")
        elif not all([len(a)==4 for a in b]): raise IndexError(f"Element of {'buttons' if n==0 else 'reversedbuttons'} must have a length of 4 characters")
        return [self.__reverse(a.upper()) if n==1 else a.upper() for a in b][::-1 if n==1 else 1]

    def __checkd(self, d, n):
        if not isinstance(d, str): raise TypeError("display must be in str" if n==0 else "reverseddisplay must be in str")
        elif len(d)!=4: raise IndexError(f"{'display' if n==0 else 'reverseddisplay'} must have a length of 4 characters")
        return self.__reverse(d.upper()) if n==1 else d.upper()
    
    def __init__(self, edgework:edgework, reverseddisplay:str|None=None, reversedbuttons:list[str]|None=None, display:str|None=None, buttons:list[str]|None=None):
        '''
        Initialize a new thirdbase instance

        Args:
            edgework (edgework): The edgework of the bomb
            display (str): The word displayed (right side up) on the module
			buttons (list [str]): The word buttons (right side up) on the module
            reverseddisplay (str): The word displayed (upside down/how you see it) on the module
            reversedbuttons (list [str]): The word buttons (upside down/how you see it) on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if display is None and buttons is None and reverseddisplay is None and reversedbuttons is None: raise TypeError("thirdbase.__init__() missing 2 required positional argument: 'display' or 'reverseddisplay' and 'buttons' or 'reversedbuttons'")        
        if display is not None: self.__display = self.__checkd(display, 0); self.__reversedd=False
        elif reverseddisplay is not None: self.__display = self.__checkd(reverseddisplay, 1); self.__reversedd=True
        else: raise TypeError("thirdbase.__init__() missing 1 required positional argument: 'display' or 'reverseddisplay'")
        if buttons is not None: self.__buttons = self.__checkb(buttons, 0); self.__reversedb=False
        elif reversedbuttons is not None: self.__buttons = self.__checkb(reversedbuttons, 1); self.__reversedb=True
        else: raise TypeError("thirdbase.__init__() missing 1 required positional argument: 'buttons' or 'reversedbuttons'")
    
    def __calculate(self, p):
        for a in self.__list[self.__buttons[p]]:
            if a in self.__buttons: return self.__buttons.index(a)

    def solve(self):
        '''
        Solve the Third Base module
        
        Returns:
		 	(int, str, bool): The index of the button, the word of that said button, and the state if the button was upside down or not (True for upside down).
        '''
        ans = self.__calculate([a for a in range(len(self.__bank)) if self.__display in self.__bank[a]][0])
        return self.__buttons.index(self.__buttons[::-1][ans]) if self.__reversedd else ans, self.__reverse(self.__buttons[ans]) if self.__reversedb else self.__buttons[ans], self.__reversedb