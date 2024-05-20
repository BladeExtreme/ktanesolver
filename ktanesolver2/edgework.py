class edgework:
    def __init__(self, batt: int, hold: int, ind: list, ports: list, sn: str, total_modules: int, strikes: int = 0):
        self.batt = batt; self.hold = hold
        self.ind = [a.upper() for a in ind]
        self._unlitind = [a.upper() for a in ind if '*' not in a]; self._litind = [a.upper() for a in ind if '*' in a]
        self.ports = [[b.upper() for b in a] for a in ports]; self._plates = len(ports); self._uniqueports = set(a for b in self.ports for a in b)
        self.sn = sn.upper()
        self._sndigit = [a for a in self.sn if a.isdigit()]; self._snletter = [a for a in self.sn if a.isalpha()]
        self.total_modules = total_modules
        self.strikes = strikes
        self.needy = 0
    
    def striked(self, i:int|None=1):
        '''
        Add 'i' to the strike counter
        
        args:
            i (int): The number to be added to the strike counter. i is by default set to 1
        '''
        self.strikes += i
    
    def needyset(self, i:int):
        '''
        Set 'i' to the total amount of needy
        
        args:
            i (int): The amount to be added to the strike counter. i is by default set to 0
        '''
        if not isinstance(i, int): raise TypeError("i must be in int")
        elif i<0: raise ValueError("i cannot be negative integer")
        self.needy = i