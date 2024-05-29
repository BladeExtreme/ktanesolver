class edgework:
    def __init__(self, batt: int, hold: int, ind: list, ports: list, sn: str, total_modules: int, needy: int, strikes: int = 0):
        self.batt = batt; self.hold = hold
        self.ind = [a.upper() for a in ind]
        self._unlitind = [a.upper() for a in ind if '*' not in a]; self._litind = [a.upper() for a in ind if '*' in a]
        self.ports = [[b.upper() for b in a] for a in ports]; self._plates = len(ports); self._uniqueports = set(a for b in self.ports for a in b)
        self.sn = sn.upper()
        self._sndigit = [a for a in self.sn if a.isdigit()]; self._snletter = [a for a in self.sn if a.isalpha()]
        self.total_modules = total_modules
        self.strikes = strikes
        self.needy = needy
    
    def striked(self, i:int|None=1):
        '''
        Add 'i' to the strike counter
        
        args:
            i (int): The number to be added to the strike counter. i is by default set to 1
        '''
        self.strikes += i