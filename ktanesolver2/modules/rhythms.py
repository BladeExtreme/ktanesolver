from ..edgework import edgework
from ..tools.colordict import _colorcheck

class rhythms(edgework):
    __table = {
        tuple(['1/4','1/6','1/4','1/6']): {'blue': ['♩2','♪P'], 'red': '***', 'green': ['♬2', '♪P'], 'yellow': ['♫2', '♪P']},
        tuple(['1/2','1/4','1/8','1/8']): {'blue': ['♩1','♬P'], 'red': ['♪P','♩P'], 'green': ['♫P', '♪1'], 'yellow': ['♫1', '♬1']},
        tuple(['1/8','1/4','1/8','1/4','1/4']): {'blue': ['♫1', '♪P'], 'red': ['♪1','♫1'], 'green': ['♩1','♬P'], 'yellow': ['♬P','♬1']},
        tuple(['5/8','1/8','1/4','1/6','1/6','1/6']): {'blue': ['♪P','♫P'], 'red': ['♬1','♩P'], 'green': ['♬1','♬P'], 'yellow': ['♫1','♪P']},
        tuple(['1/8','1/8','1/4','1/2']): {'blue': ['♪1','♫P'], 'red': ['♬P','♫P'], 'green': ['♩1','♪P'], 'yellow': ['♬P','♫1']},
        tuple(['1/4','1/2','1/6','1/6','1/6']): {'blue': ['♩1','♬1'], 'red': ['♪P','♪1'], 'green': ['♫P', '♪P'], 'yellow': ['♫P', '♩1']},
        tuple(['1/4','1/4','1/4','1/4']): {'blue': ['♩P','♪1*'], 'red': ['♫P','♫1*'], 'green': ['♬P','♬1*'], 'yellow': ['♪P', '♪P*']}
    }
    
    def __check(self, c, r):
        if not isinstance(c, str): raise TypeError("color must be in str")
        elif not isinstance(r, list): raise TypeError("rhythm must be in list")
        elif not all([isinstance(a, str) for a in r]): raise TypeError("Element of rhythm must be in str")
        elif not all([a in ['1/2','5/8','1/4','1/6','1/8','1/16'] for a in r]): raise ValueError("This note notation isn't available in the stored list. Use showNotes()")
        return _colorcheck(c.lower()), r
    
    def __init__(self, edgework:edgework, color:str, rhythm:list[str]):
        '''
        Initialize a new rhythms instance

        Args:
            edgework (edgework): The edgework of the bomb
            color (str): The color of the light that is flashing
            rhythm (list (str)): The rhythm that is being flashed. Use number notation (1/2, 1/4, 1/8, 1/16). Order is important, starting note does not matter. Use showNotes() for more information
        NOTE:
            If you're unsure about the notation that is being used to represents the rhythm, use showNotes()
            If you're unsure what sequence is being flashed, use showSequence()
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color, self.__rhythm = self.__check(color, rhythm)
        for x in range(len(self.__rhythm)):
            self.__rhythm = self.__rhythm[1:]+[self.__rhythm[0]]
            if tuple(self.__rhythm) in self.__table:
                break
    
    def showNotes(self):
        temp = {
            '1/2': 'notation for note that lasts for two beats',
            '5/8': 'notation for note that lasts for one and a half beat',
            '1/4': 'notation for note that lasts for one beat',
            '1/6': 'notation for note that plays on third of a beat',
            '1/8': 'notation for note that lasts for half a beat',
            '1/16': 'notation for note that lasts for quarter of a beat'
        }
        return [{a: b} for a,b in temp.items()]
    def showSequences(self):
        return [a for a in self.__table.keys()]
    
    def __calculate(self):
        order = "P123456789"
        temp = self.__table[tuple(self.__rhythm)][self.__color]; ans = []
        if temp=='***': return ['spam']
        for a in temp:
            temp2 = []
            if '*' in a and self.batt>1: temp2.append(ans[0][0])
            elif a[0]=='♩': temp2.append('1/4')
            elif a[0]=='♪': temp2.append('1/8')
            elif a[0]=='♫': temp2.append('beamed 1/8')
            elif a[0]=='♬': temp2.append('beamed 1/16')
            if self.__color=='yellow':
                temp2.append(order[order.index(a[1])+len(self._litind)])
            else: temp2.append(a[1])
            ans.append(tuple(temp2))
        return ans
    
    def solve(self):
        '''
        Solve the Rhythms module

        Returns:
            tuple (tuple (str)): The correct button press/hold according to its label. Each index 0 of sub-tuples, are the note that needs to be pressed or hold. Index 1 of each sub-tuples are the duration of that button needed to be pressed down. If it's "P", it means press otherwise hold the button down for that amount of beep when pressing down
        '''
        return tuple(self.__calculate())