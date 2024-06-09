class edgework:
    def __init__(self, batt: int, hold: int, ind: list, ports: list, sn: str, total_modules: int, needy: int, strikes: int = 0):
        self.batt = batt; self.hold = hold
        self.ind = [a.upper() for a in ind]
        self._unlitind = [a.upper() for a in ind if '*' not in a]; self._litind = [a.upper() for a in ind if '*' in a]
        self.ports = self.__portnamechecker([[b.upper() for b in a] for a in ports]); self._plates = len(ports); self._uniqueports = set(a for b in self.ports for a in b)
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
    
    def __portnamechecker(self, a):
        for c in range(len(a)):
            for b in range(len(a[c])):
                if any([d == a[c][b] for d in ['PS2', 'PS/2']]): a[c][b] = 'PS/2'
                elif any([d == a[c][b] for d in ['RCA', 'STEREO RCA']]): a[c][b] = 'STEREO RCA'
                elif any([d == a[c][b] for d in ['RJ-45','RJ45','RJ','RJ 45','RJ-45']]): a[c][b] = 'RJ-45'
                elif any([d == a[c][b] for d in ['DVI', 'DVID', 'DVI D', 'DVI-D']]): a[c][b] = 'DVI-D'
                elif any([d == a[c][b] for d in ['PAR', 'PARALLEL']]): a[c][b] = 'PARALLEL'
                elif any([d == a[c][b] for d in ['SER', 'SERIAL']]): a[c][b] = 'SERIAL'
                else:
                    raise ValueError(f"Port name/abbreviation cannot be found. {a[c][b]}")
        return a