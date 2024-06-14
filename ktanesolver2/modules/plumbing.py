from ..edgework import edgework

class plumbing(edgework):
    def __init__(self, edgework:edgework):
        '''
        Initialize a new plumbing instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
    
    def __calculate(self):
        inputred = (1 if '1' in self._sndigit else 0)+(1 if 'RJ-45' in self._uniqueports else 0)-(1 if len(self._uniqueports)!=len([a for b in self.ports for a in b]) else 0)-(1 if len(self.sn)!=len(set(self.sn)) else 0)
        inputyel = (1 if '2' in self._sndigit else 0)+(1 if [a for b in self.ports for a in b].count('STEREO RCA')>=1 else 0)-(1 if len(self._uniqueports)==len([a for b in self.ports for a in b]) else 0)-(1 if '1' in self._sndigit or 'L' in self._snletter else 0)
        inputgrn = (1 if len(self._sndigit)>=3 else 0)+(1 if [a for b in self.ports for a in b].count("DVI-D")>=1 else 0)-(1 if inputred<1 else 0)-(1 if inputyel<1 else 0)
        inputblu = (99 if inputred<1 and inputyel<1 and inputgrn<1 else 0)+(1 if len(self._uniqueports)>=4 else 0)+(1 if self.batt>=4 else 0)-(1 if len([a for b in self.ports for a in b])==0 else 0)-(1 if self.batt==0 else 1)
        inputs = [inputred, inputyel, inputgrn, inputblu]; inputs = list(map(lambda x: x>=1, inputs))

        outputred = (1 if [a for b in self.ports for a in b].count("SERIAL")>=1 else 0)+(1 if self.batt==1 else 0)-(1 if len(self._sndigit)>2 else 0)-(1 if inputs.count(True)>2 else 0)
        outputgrn = (1 if )
        # outputyel = 
    
    def solve(self):
        return self.__calculate()