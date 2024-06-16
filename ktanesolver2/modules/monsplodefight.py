from ..edgework import edgework

class monsplodefight(edgework):
    def __check(self, m, v, n):
        if not isinstance(m, str): raise TypeError("monsplode must be in str")
        elif not isinstance(v, list): raise TypeError("moves must be in list")
        elif not isinstance(n, int): raise TypeError("remainingminutes must be in int")
        elif n<0: raise ValueError("remainingminutes must be positive")
        elif not all([isinstance(a, str) for a in v]): raise TypeError("Element of moves must be in str")
        elif len(v)!=4: raise IndexError("Length of moves must be 4")
        return m.lower(), [a.lower() for a in v], n
    
    def __init__(self, edgework:edgework, monsplode:str, moves:list, remainingminutes:int, firstmodule:bool|None=False, finalmodulle:bool|None=False):
        '''
        Initialize a new monsplodefight instance

        Args:
            edgework (edgework): The edgework of the bomb
            monsplode (str): The name of the monsplode that appears
            moves (list (str)): The possible movelists
            remainingminutes (int): The remaining time on bomb in minutes. Seconds ignored
            firstmodule (bool): Is this monsplodefight the first module to be solved in a bomb? By default False
            finalmodule (bool): Is this monsplodefight the last module to be solved in a bomb? By default False
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__monsplode, self.__moves, self.__remainingminutes = self.__check(monsplode, moves, remainingminutes)
        self.__finalmodule = finalmodulle if isinstance(finalmodulle, bool) else -1
        self.__firstmodule = firstmodule if isinstance(firstmodule, bool) else -1
        if self.__finalmodule==-1: raise TypeError("finalmodule must be bool")
        elif self.__firstmodule==1: raise TypeError("firstmodule must be bool")
        elif self.__firstmodule and self.__finalmodule: raise ValueError("firstmodule and falsemodule cannot be True together")
    
    def __calculate(self):
        monsplodelist = {
            "buhar": {"type": "water", "rule": lambda x: [0 if a['type']=='rock' else a['damage'] for a in x]},
            "lanaluff": {'type': 'normal', 'rule': lambda x: [a['damage']+3 if a['type']=='poison' and any([c in set(["LANALUFF"]) for c in self._snletter]) else a['damage'] for a in x]},
            "bob": {'type': 'normal', 'rule': lambda x: [0 if a['type']!='normal' and 'BOB*' in self._litind else a['damage'] for a in x]},
            "mountoise": {"type": "rock" if self.strikes==0 else "normal", "rule": lambda x: [a['damage'] for a in x]},
            "nibs": {'type': 'normal', 'rule': lambda x: [0 if a['type']=='grass' else a['damage'] for a in x]},
            "aluga": {'type': 'normal', 'rule': lambda x: [a['damage']+2 if a['type']=='fire' else a['damage']-1 if a['type']=='water' else a['damage'] for a in x]},
            "lugirit": {'type': 'ghost', 'rule': lambda x: [a['damage']+2 if a['type']=='water' else a['damage']-1 if a['type']=='fire' else a['damage'] for a in x]},
            "caadarim": {'type': 'normal', 'rule': lambda x: [0 if a['type']=='normal' and len(self._uniqueports)>0 else a['damage'] for a in x]},
            "vellarim": {'type': 'water', 'rule': lambda x: [0 if a['type']=='normal' and 'PARALLEL' in self._uniqueports else a['damage'] for a in x]},
            "flaurim": {'type': 'fire', 'rule': lambda x: [0 if a['type']=='normal' and 'SERIAL' in self._uniqueports else a['damage'] for a in x]},
            "gloorim": {'type': 'dark', 'rule': lambda x: [0 if a['type']=='normal' and 'DVI-D' in self._uniqueports else a['damage'] for a in x]},
            "melbor": {'type': 'dark', 'rule': lambda x: [0 if a['damage']==6 or a['damage']==8 else a['damage'] for a in x]},
            "clondar": {'type': 'electric', 'rule': lambda x: [a['damage']+3 if a['type']=='water' else a['damage'] for a in x]},
            "docsplode": {'type': 'normal', 'rule': lambda x: [0 if self.__moves.count('boom')!=0 and self.__moves[a]!='boom' else 99 if self.__moves.count('boom')!=0 and self.__moves[a]=='boom' else x[a]['damage'] for a in range(len(x))]},
            "magmy": {'type': 'fire' if self.batt>=3 else 'rock', 'rule': lambda x: [a['damage'] for a in x]},
            "pouse": {'type': 'electric', 'rule': lambda x: [0 if a['damage']==6 else ['damage'] for a in x]},
            "ukkens": {'type': 'poison', 'rule': lambda x: [0 if a['type']=='water' else a['damage'] for a in x]},
            "asteran": {'type': 'grass' if 'CAR' not in self.ind and 'CAR*' in self.ind else 'water', 'rule': lambda x: [a['damage'] for a in x]},
            "violan": {'type': 'grass' if 'CLR' not in self.ind and 'CLR*' in self.ind else 'water', 'rule': lambda x: [a['damage'] for a in x]},
            "zenlad": {'type': 'grass', 'rule': lambda x: [a['damage']+3 if a['type']=='electric' else a['damage'] for a in x]},
            "zapra": {'type': 'electric' if self.batt>=3 else 'normal', 'rule': lambda x: [a['damage'] for a in x]},
            "myrchat": {'type': 'poison' if len(self._litind)>0 else 'dark', 'rule': lambda x: [a['damage'] for a in x]},
            "percy": {'type': 'water', 'rule': lambda x: [0 if self.__moves.count('splash')!=0 and self.__moves[a]!='splash' else 99 if self.__moves.count('splash')!=0 and self.__moves[a]=='splash' else x[a]['damage'] for a in range(len(x))]},
            "cutie pie": {'type': 'normal', 'rule': lambda x: [99 if a['damage']==min([b['damage'] for b in x]) else 0 for a in x]}
        }
        montype, monrule = monsplodelist[self.__monsplode]['type'], monsplodelist[self.__monsplode]['rule']

        movelist = {
            "appearify": {'type': 'normal', 'damage': 4 if montype!='dark' else 10},
            "battery power": {'type': 'electric', 'damage': 0+(2*self.batt)},
            "bedrock": {'type': 'rock', 'damage': 0+(1*self.total_modules)},
            "boo": {'type': 'ghost', 'damage': 0+(3*self._snletter.count('O')+3*self._sndigit.count('0'))},
            "boom": {'type': 'fire', 'damage': 0},
            "bug spray": {'type': 'poison', 'damage': 2 if self.__monsplode!='melbor' and self.__monsplode!='zenlad' else 10},
            "countdown": {'type': 'poison', 'damage': 0+self.__remainingminutes},
            "dark portal": {'type': 'dark', 'damage': 0+len([a for b in self.ports for a in b])},
            "fiery soul": {'type': 'fire', 'damage': 0+(self.batt*self.hold)},
            "finale": {'type': 'grass', 'damage': 2 if not self.__finalmodule else 10},
            "freak out": {'type': 'ghost', 'damage': 10 if 'FRK*' in self._litind or 'FRQ*' in self._litind else 5 if 'FRK' in self._unlitind or 'FRQ' in self._unlitind else 1},
            "glyph": {'type': 'normal', 'damage': 0+len(self.__monsplode)},
            "last word": {'type': 'ghost', 'damage': 0+int(self._sndigit[-1])},
            "sendify": {'type': 'normal', 'damage': 10 if montype=='grass' or montype=='rock' else 2},
            "shock": {'type': 'electric', 'damage': 8 if 'RJ-45' in self._uniqueports else 3},
            "shrink": {'type': 'normal', 'damage': 0+min([int(a) for a in self._sndigit])},
            "sidestep": {'type': 'normal', 'damage': 0+len(self.__moves[self.__moves.index("sidestep")-1] if self.__moves.count('sidestep')>0 and self.__moves.index("sidestep")%2==1 else self.__moves[self.__moves.index("sidestep")+1] if self.__moves.count('sidestep')>0 else '')},
            "stretch": {'type': 'normal', 'damage': 0+max([int(a) for a in self._sndigit])},
            "void": {'type': 'dark', 'damage': 10 if self.__firstmodule else 2},
            "defuse": {'type': 'dark', 'damage': 999},
            
            "candle": {'type': 'fire', 'damage': 2},                      "spectre": {'type': 'ghost', 'damage': 5},
            "cave in": {'type': "rock", 'damage': 3},                     "splash": {'type': 'water', 'damage': 0},
            "double zap": {'type': 'electric', 'damage': 4},              "tac": {'type': 'normal', 'damage': 5},
            "earthquake": {'type': 'rock', 'damage': 5},                  "tangle": {'type': 'grass', 'damage': 2}, 
            "flame spear": {'type': 'fire', 'damage': 6},                 "tic": {'type': 'normal', 'damage': 3},
            "fountain": {'type': 'water', 'damage': 6},                   "toe": {'type': 'normal', 'damage': 1},
            "grass blade": {'type': 'grass', 'damage': 4},                "torchlight": {'type': 'fire', 'damage': 4},
            "heavy rain": {'type': 'water', 'damage': 4},                 "toxic": {'type': 'poison', 'damage': 5},
            "high voltage": {'type': 'electric', 'damage': 6},            "venom fang": {'type': 'poison', 'damage': 3},
            "hollow gaze": {'type': 'dark', 'damage': 4},                 "zap": {'type': 'electric', 'damage': 2},
            "ivy spikes": {'type': 'grass', 'damage': 6}
        }
        multiplierlist = {
            'normal'    : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*0.5, 'ghost': lambda x: x*0, 'fire': lambda x: x*1, 'water': lambda x: x*1, 'grass': lambda x: x*1, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'poison'    : {'normal': lambda x: x*1, 'poison': lambda x: x*0.5, 'rock': lambda x: x*0.5, 'ghost': lambda x: x*0.5, 'fire': lambda x: x*1, 'water': lambda x: x*1, 'grass': lambda x: x*2, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'rock'      : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*1, 'ghost': lambda x: x*1, 'fire': lambda x: x*2, 'water': lambda x: x*1, 'grass': lambda x: x*1, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'ghost'     : {'normal': lambda x: x*0, 'poison': lambda x: x*1, 'rock': lambda x: x*1, 'ghost': lambda x: x*2, 'fire': lambda x: x*1, 'water': lambda x: x*1, 'grass': lambda x: x*1, 'electric': lambda x: x*1, 'dark': lambda x: x*0.5},
            'fire'      : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*0.5, 'ghost': lambda x: x*1, 'fire': lambda x: x*0.5, 'water': lambda x: x*0.5, 'grass': lambda x: x*2, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'water'     : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*2, 'ghost': lambda x: x*1, 'fire': lambda x: x*2, 'water': lambda x: x*0.5, 'grass': lambda x: x*0.5, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'grass'     : {'normal': lambda x: x*1, 'poison': lambda x: x*0.5, 'rock': lambda x: x*2, 'ghost': lambda x: x*1, 'fire': lambda x: x*0.5, 'water': lambda x: x*2, 'grass': lambda x: x*0.5, 'electric': lambda x: x*1, 'dark': lambda x: x*1},
            'electric'  : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*1, 'ghost': lambda x: x*1, 'fire': lambda x: x*1, 'water': lambda x: x*2, 'grass': lambda x: x*0.5, 'electric': lambda x: x*0.5, 'dark': lambda x: x*1},
            'dark'      : {'normal': lambda x: x*1, 'poison': lambda x: x*1, 'rock': lambda x: x*1, 'ghost': lambda x: x*2, 'fire': lambda x: x*1, 'water': lambda x: x*1, 'grass': lambda x: x*1, 'electric': lambda x: x*1, 'dark': lambda x: x*0.5},
        }
        damages = [movelist[self.__moves[a]] for a in range(4)]
        damages = [{'type': a['type'], 'damage': multiplierlist[a['type']][montype](a['damage'])} for a in damages]
        damages = monrule(damages)
        damagetouse = self.__moves[damages.index(max(damages))]
        return damagetouse

    def solve(self):
        '''
        Solve the Monsplode, Fight! module

        Returns:
            str: The correct move that should be used
        '''
        return self.__calculate()