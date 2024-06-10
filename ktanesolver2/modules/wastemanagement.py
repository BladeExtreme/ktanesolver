from ..edgework import edgework

class wastemanagement(edgework):
    def __init__(self, edgework:edgework, morethanhalf:bool=False, lastfifth:bool=False, morseexist:bool=False, fmnexist:bool=False):
        '''
        Initialize a new wastemanagement instance

        Args:
            edgework (edgework): The edgework of the bomb
            morethanhalf (bool): The state if the bomb's timer pasts its halftime after a strike or a single submit on waste management
            lastfifth (bool): The state if the bomb's timer pasts its 4/5th its time after a strike or a single submit on waste management
            morseexist (bool): State if bomb has other modules with 'Morse' in it or 'Simon Sends' exist in it
            fmnexist (bool): State if bomb has a module called 'Forget Me Not' in it
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if not isinstance(morethanhalf, bool): raise TypeError("morethanhalf must be in bool")
        if not isinstance(lastfifth, bool): raise TypeError("lastfifth must be in bool")
        if not isinstance(morseexist, bool): raise TypeError("morseexist must be in bool")
        if not isinstance(fmnexist, bool): raise TypeError("fmnexist must be in bool")
        self.__morehalf = morethanhalf
        self.__morseexist = morseexist
        self.__fmnexist = fmnexist
        self.__lastfifth = lastfifth
    
    def __papercalculate(self):
        paper = 0
        if ('IND' in self._unlitind or 'IND*' in self._litind) and self.batt<5: paper+=19
        if ('SND' in self._unlitind or 'SND*' in self._litind): paper+=15
        if 'PARALLEL' in self._uniqueports: paper-=44
        if self.__morseexist and self.__morehalf: paper-=26
        if self.batt==0 and len(self.ind)<3: paper+=154
        if any([a in [b for b in 'SAVEMYWORLD'] for a in self._snletter]) and len(self._snletter)-len([a for a in self._snletter if a in ['A','I','U','E','O']])<=2: paper+=200
        return paper

    def __plasticcalculate(self):
        plastic = 0
        if ('TRN' in self._unlitind or 'TRN*' in self._litind) and self.strikes!=1: plastic+=91
        if ('FRK' in self._unlitind or 'FRK*' in self._litind) and self.strikes!=2: plastic+=69
        if [] in self.ports and (self.total_modules+self.needy)%2==0: plastic-=17
        if ('FRQ' in self._unlitind or 'FRQ*' in self._litind) and not (self.batt-(self.batt-self.hold)*2)>(self.batt-self.hold)*2: plastic+=153
        return plastic

    def __metalcalculate(self):
        metal = 0
        if ('BOB' in self._unlitind or 'BOB*' in self._litind): metal+=199
        if ('MSA' in self._unlitind or 'MSA*' in self._litind): metal+=92
        if ('CAR' in self._unlitind or 'CAR*' in self._litind) and 'RJ-45' not in self._uniqueports: metal-=200
        if self.ports!=[] and self._uniqueports!=set([a for b in self.ports for a in b]) and 'DVI-D' not in self._uniqueports:
            metal+=153
        if ('SIG' in self._unlitind or 'SIG*' in self._litind) and not self.__lastfifth: metal+=99
        if self.__fmnexist:
            if 'BOB*' in self._litind and len([a for b in self.ports for a in b])>=6: metal+=99
            else: metal-=84
        return metal

    def __round(self, n):
        return int(n)+(1 if (int(n)*2)-int((n/0.5))==-1 else 0)

    def solve(self):
        paper = abs(self.__papercalculate())
        plastic = abs(self.__plasticcalculate())
        metal = abs(self.__metalcalculate())
        leftovers = 0

        recycle= {'paper': 0, 'plastic': 0, 'metal': 0, 'leftovers': 0}; waste= {'paper': 0, 'plastic': 0, 'metal': 0, 'leftovers': 0}
        stage=1

        while(stage!=-1):
            flag=False
            if paper+plastic+metal>695 and stage==1:
                recycle['paper'] = paper; recycle['plastic'] = plastic; recycle['metal'] = metal
                paper=plastic=metal=0
                stage=-1
            if metal>200 and stage==2:
                recycle['metal'] = self.__round((3/4)*metal); waste['metal'] = metal-self.__round((3/4)*metal)
                metal-=metal
                stage=4; flag=True
            if metal<paper and stage==3:
                recycle['paper'] = paper; leftovers=plastic; waste['metal'] = self.__round((1/4)*metal); recycle['leftovers'] = self.__round(leftovers*(1/2))
                paper-=paper; plastic-=plastic; metal-=self.__round((1/4)*metal)
                stage=-1
            if plastic in range(101,300) and stage==4:
                recycle['plastic'] = self.__round(plastic*(1/2)); plastic=plastic-self.__round(plastic*(1/2))
                stage=6
            if plastic in range(11, 100) and stage==5: waste['plastic'] = plastic; plastic-=plastic
            if paper<65 and stage==6: 
                if flag: waste['paper']=paper; paper-=paper
                else:
                    waste['paper']=self.__round((1/3)*paper)
                    paper-=self.__round((1/3)*paper)
            if stage==7: leftovers+=metal; leftovers+=paper; leftovers+=plastic
            if leftovers in range(101,300) and stage==7: recycle['leftovers'] = leftovers
            elif stage==7: waste['leftovers'] = leftovers
            stage = (stage+1 if stage<7 and stage!=-1 else -1)
        
        return recycle, waste