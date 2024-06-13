from ..edgework import edgework

class painting(edgework):
    def __init__(self, edgework:edgework):
        '''
        Initialize a new painting instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
    
    def __calculate(self):
        colorchange = [
            {'black': 'red', 'gray': 'gray', 'red': 'red', 'brown': 'green', 'orange': 'orange', 'yellow': 'yellow', 'green': 'green', 'blue': 'red', 'purple': 'pink', 'pink': 'purple',},
            {'black': 'black', 'gray': 'gray', 'red': 'green', 'brown': 'purple', 'orange': 'orange', 'yellow': 'green', 'green': 'yellow', 'blue': 'pink', 'purple': 'brown', 'pink': 'gray',},
            {'black': 'purple', 'gray':'blue', 'red': 'orange', 'brown': 'brown', 'orange': 'red', 'yellow': 'yellow', 'green': 'blue', 'blue': 'gray', 'purple': 'black', 'pink': 'pink',}
        ]
        
        flatports = [a for b in self.ports for a in b]
        if flatports.count('DVI-D')==2 and flatports.count('RJ-45')==1 and 'CLR*' in self._litind:
            temp = {}
            for a in colorchange[0]:
                temp[a] = 'any'
            return temp

        blindtype = ['protanomaly','deuteranomaly','tritanopia']
        score = [0,0,0]; distinctletters = set([a for b in self.ind for a in b if a!='*']); use = -1
        for a in range(3):
            if len(blindtype[a])==self.batt+len(self.ind)+len([a for b in self.ports for a in b]): use=a
            score[a] = sum([blindtype[a].count(b.lower()) for b in distinctletters])
        if use==-1:
            if score.count(max(score))==1: use = score.index(max(score))
            else: use = 0
        return colorchange[use]

    def solve(self):
        '''
        Solve the Painting module

        Returns:
            dict: The dict of the color switches. Values for each key are the new color after the switch, some doesn't change. Keys only consists of the following: 'black', 'gray', 'red', 'brown', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'
        '''
        return self.__calculate()