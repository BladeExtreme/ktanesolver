from ..edgework import edgework
from ..tools.colordict import _colorcheck

class resistors(edgework):
    __table = {
        'black': ['0','0',str(10**0)],
        'brown': ['1','1',str(10**1)],
        'red': ['2','2',str(10**2)],
        'orange': ['3','3',str(10**3)],
        'yellow': ['4','4',str(10**4)],
        'green': ['5','5',str(10**5)],
        'blue': ['6','6',str(10**6)],
        'violet': ['7','7',str(10**7)],
        'gray': ['8','8',None],
        'white': ['9','9',None],
        'gold': [None,None,str(10**(1/2))],
        'silver': [None,None,str(10**(1/4))]
    }
    
    def __check(self, r):
        if not isinstance(r, list): raise TypeError("resistor_colors must be in list")
        elif len(r)!=2: raise IndexError("Length of resistor_colors must be 2")
        elif not all([isinstance(a, list) for a in r]): raise TypeError("Element of resistor_colors must be in list")
        elif not all([isinstance(a, str) for a in r[0]]) or not all([isinstance(a, str) for a in r[1]]): raise TypeError("Element of resistor_colors sublists must be in str")
        elif len(r[0])!=3 or len(r[1])!=3: raise IndexError("Length of each resistor_colors sublists must be 3")
        elif not all([_colorcheck(a.lower()) in ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white', 'gold', 'silver'] for a in r[0]+r[1]]): raise ValueError("Values of resistor_colors sublists must be in 'black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white', 'gold' or 'silver'")
        return [[_colorcheck(b.lower()) for b in a] for a in r]
    
    def __init__(self, edgework:edgework, resistor_colors:list[list[str]]):
        '''
        Initialize a new resistor instance

        Args:
            edgework (edgework): The edgework of the bomb
            resistor_colors (list [list [str]]): The color band that appears on each resistors. Each sub-lists represents the color bands for each resistors. Index 0 from main list is the top resistor, index 1 from main list is the bottom resistor. The fourth color band (separated by a gap from 3 color bands) are ignored. Order matters, index 0 of each sub lists represents the first color band (leftmost) and index 3 of each sub lists represents the last color band (rightmost). NOTE: Some resistors can be mirrored, in that case the index 0 color band is the rightmost.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__color = self.__check(resistor_colors)
    
    def __calculate(self):
        resistor_val = [int("".join([self.__table[a[0]][0],self.__table[a[1]][1]]))*int(self.__table[a[2]][2]) for a in self.__color]
        prim_in = 'A' if int(self._sndigit[0])%2==0 else 'B'; sub_in = 'B' if prim_in=='A' else 'A'
        prim_out = 'C' if int(self._sndigit[-1])%2==0 else 'D'; sub_out = 'D' if prim_out=='C' else 'C'
        both_output = False; added = []

        if "FRK*" in self._litind: both_output = True
        elif self.batt-(self.batt-self.hold)>=1: added = [[f'{sub_in}', f'{sub_out}']]

        pathway = ''
        target = int("".join([a for a in self._sndigit[:2]]))*(10**self.batt)
        if target>10**6: target = 10**6
        
        if target==0: pathway = 'instant'
        elif any([target==a for a in resistor_val]): pathway = str([a for a in range(len(resistor_val)) if resistor_val[a]==target][0])
        elif target>resistor_val[0] and target>resistor_val[1]: pathway = 'series'
        elif target<resistor_val[0] and target<resistor_val[1]: pathway = 'parallel'

        if pathway=='instant': return [[f'{prim_in}', f'{prim_out}']]+[[f'{prim_in}', f'{sub_out}'] if both_output else []]+added
        elif pathway=='series': return [[f'{prim_in}', f'Top Resistor'], ["Top Resistor", f'{prim_out}']]+[["Top Resistors", f'{sub_out}'] if both_output else []]+added
        elif pathway=='parallel': return [[f'{prim_in}', "Top Resistor"], [f"{prim_in}", "Bottom Resistor"], ["Top Resistor", f'{prim_out}'], ["Bottom Resistor", f'{prim_out}']]+[["Top Resistor", f'{sub_out}'] if both_output else []]+[["Bottom Resistor", f'{sub_out}'] if both_output else []]+added
        else:
            return [[f'{prim_in}', f'{"Top Resistor" if pathway==str(0) else "Bottom Resistor"}'],[f'{"Top Resistor" if pathway==str(0) else "Bottom Resistor"}', {prim_out}]]+[[f'{"Top Resistor" if pathway==str(0) else "Bottom Resistor"}', {sub_out}] if both_output else []]+added

    def solve(self) -> list[list[str]]:
        '''
        Solve the Resistors module

        Returns:
            list [list [str]]: Returns the order of which resistor should it connect to and which input/out should be used. Order does not matter
        '''
        result = self.__calculate()
        return [a for a in result if a!=[]]