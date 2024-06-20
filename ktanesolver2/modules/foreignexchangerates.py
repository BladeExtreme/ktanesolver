from ..edgework import edgework
from ..tools.colordict import _colorcheck

class foreignexchangerates(edgework):
    def __check(self, l,b):
        if not isinstance(l, str): raise TypeError("lightcolor must be in str")
        elif not isinstance(b, list): raise TypeError("buttons must be in list")
        elif len(b)!=3: raise TypeError("Length of buttons must be 3")
        elif not all([isinstance(a, str) for a in b]): raise TypeError("Element of buttons must be in str")
        elif not all([len(a)==3 for a in b]): raise IndexError("Element of buttons must have a length of 3 characters/numbers")
        return _colorcheck(l.lower()), [a.upper() for a in b]
    def __check2(self, x):
        if not isinstance(x, float): raise TypeError("rates must be in float")
        return x
    
    def __init__(self, edgework:edgework, lightcolor:str, buttons:list[str]):
        '''
        Initialize a new foreignexchangerates instance

        Args:
            edgework (edgework): The edgework of the bomb
            lightcolor (str): The color of the light above each button on the module
            buttons (list [str]): The buttons from top row to bottom row. Each element must be contain 3 letter/numbers
        NOTE:
            IMPORTANT!
            As of 20/06/2024, I cannot find a way to access to fer.eltrick.uk. This is because it requires an access code via python but not from websites. A help would be nice!
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__lightcolor, self.__buttons = self.__check(lightcolor,buttons)
    
    def __calculate(self):
        code = {'036': 'AUD','124': 'CAD','156': 'CNY','191': 'HRK','208': 'DKK','344': 'HKD','348': 'HUF','356': 'INR','360': 'IDR','376': 'ILS','392': 'JPY','410': 'KRW','458': 'MYR','484': 'MXN','554': 'NZD','578': 'NOK','608': 'PHP','643': 'RUB','702': 'SGD','710': 'ZAR','752': 'SEK','756': 'CHF','764': 'THB','826': 'GBP','840': 'USD','946': 'RON','949': 'TRY','975': 'BGN','978': 'EUR','985': 'PLN','986': 'BRL'}
        base = (self.__buttons[0] if self.__buttons[0].isalpha() else code[self.__buttons[0]]) if self.batt<2 else (self.__buttons[1] if self.__buttons[1].isalpha() else code[self.__buttons[1]])
        target = (self.__buttons[1] if self.__buttons[1].isalpha() else code[self.__buttons[1]]) if self.batt<2 else (self.__buttons[0] if self.__buttons[0].isalpha() else code[self.__buttons[0]])
        if self.__lightcolor=='green' and self.__multiplier==None:
            return f"https://fer.eltrick.uk/latest?base={base}&symbols={target}"
        elif self.__lightcolor=='green':
            n = str(int(self.__multiplier*int(self.__buttons[2])))[1]
            return tuple([int(n)-1, [a for b in self.__buttons for a in b][int(n)-1 if int(n) !=0 else 0]])
        else:
            for a,b in code.items():
                if b==target: return tuple([int(a[1])-1, [x for y in self.__buttons for x in y][int(a[1])-1 if int(a[1])!=0 else 0]])
    
    def solve(self, rates:float|None=None):
        '''
        Solve the Foreign Exchange Rates

        Args:
            rates (float|None): The rates between the base and target currency
        Returns:
            str: The link to get the rates of between the base currecny and target currency
            tuple (int, str): The information of which button to press. Index 0 represents the index of the button in reading order (starting from 0), index 1 represents the character of that button
        '''
        self.__multiplier = self.__check2(rates) if rates is not None else None
        return self.__calculate()