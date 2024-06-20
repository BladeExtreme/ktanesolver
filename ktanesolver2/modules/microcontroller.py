from ..edgework import edgework

class microcontroller(edgework):
    def __check(self, c,t,s):
        if not isinstance(c, str): raise TypeError("controller must be in str")
        elif not isinstance(t, int): raise TypeError("totalpins must be in str")
        elif not isinstance(s, str): raise TypeError("serialnumber must be in str")
        elif c.upper() not in ['STRK','LEDS','CNTD','EXPL']: raise ValueError("controller type must be either: 'STRK','LEDS','CNTD','EXPL'")
        elif t not in [6,8,10]: raise ValueError("total pins must be either: 6, 8, 10")
        return c.upper(), t, s

    def __init__(self, edgework:edgework, controller:str, totalpins:int, serialnumber:str):
        '''
        Initialize a new microcontroller instance

        Args:
            edgework (edgework): The edgework of the bomb
            controller (str): The controller type (the giant letters)
            totalpins (int): Total pins of the controller
            serialnumber (str): The serial number of microcontroller
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__controller, self.__totalpins, self.__serialnumber = self.__check(controller, totalpins, serialnumber)
    
    def __calculate(self):
        table = {
            'VCC': ['yellow', 'yellow', 'red', 'red', 'green'],
            'AIN': ['magenta', 'red', 'magenta', 'blue', 'red'],
            'DIN': ['green', 'magenta', 'green', 'yellow', 'yellow'],
            'PWM': ['blue', 'green', 'blue', 'green', 'blue'],
            'RST': ['red', 'blue', 'yellow', 'magenta', 'magenta']
        }
        col = 0 if int(self.__serialnumber[-1]) in [1,4] else 1 if ('SIG*' in self._litind or 'RJ-45' in self._uniqueports) else 2 if any([a in "CLRX18" for a in self.sn]) else 3 if int(self.__serialnumber[1])==self.batt else 4
        VCC=table['VCC'][col]; AIN = table['AIN'][col]; DIN = table['DIN'][col]; PWM=table['PWM'][col]; RST=table['RST'][col]

        GND = 'white'

        pins = {
            'STRK': {
                6: {1: AIN, 2: VCC, 3: RST, 4: DIN, 5: PWM, 6: GND},
                8: {1: AIN, 2: PWM, 3: GND, 4: DIN, 5: VCC, 6: GND, 7: RST, 8: GND},
                10: {1: GND, 2: GND, 3: GND, 4: GND, 5: AIN, 6: DIN, 7: GND, 8: VCC, 9: RST, 10: PWM}},
            'LEDS': {
                6: {1: PWM, 2: RST, 3: VCC, 4: DIN, 5: AIN, 6: GND},
                8: {1: PWM, 2: DIN, 3: VCC, 4: GND, 5: AIN, 6: GND, 7: RST, 8: GND},
                10: {1: PWM, 2: AIN, 3: DIN, 4: GND, 5: GND, 6: GND, 7: GND, 8: RST, 9: VCC, 10: GND}
            },
            'CNTD': {
                6: {1: GND, 2: AIN, 3: PWM, 4: VCC, 5: DIN, 6: RST},
                8: {1: PWM, 2: GND, 3: GND, 4: VCC, 5: AIN, 6: GND, 7: DIN, 8: RST},
                10: {1: PWM, 2: DIN, 3: AIN, 4: GND, 5: GND, 6: VCC, 7: GND, 8: GND, 9: RST, 10: GND}
            },
            'EXPL': {
                6: {1: PWM, 2: VCC, 3: RST, 4: AIN, 5: DIN, 6: GND},
                8: {1: AIN, 2: GND, 3: RST, 4: GND, 5: VCC, 6: GND, 7: DIN, 8: PWM},
                10: {1: RST, 2: DIN, 3: VCC, 4: GND, 5: GND, 6: GND, 7: AIN, 8: GND, 9: PWM, 10: GND}
            }
        }
        return pins[self.__controller][self.__totalpins]
    
    def solve(self):
        '''
        Solve the Microcontroller module

        Returns:
            dict (int, str): The correlating pin number with what color. The key is the pin, the value is the color
        '''
        return self.__calculate()