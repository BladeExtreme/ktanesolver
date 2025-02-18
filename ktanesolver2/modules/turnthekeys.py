from .password import password
from .whosonfirst import whosonfirst
from .crazytalk import crazytalk
from .keypad import keypad
from .listening import listening
from .orientationcube import orientationcube
from .morsecode import morsecode
from .wires import wires
from .twobits import twobits
from .button import button
from .colourflash import colourflash
from .roundkeypad import roundkeypad

class turnthekeys:
    __listL = [password, whosonfirst, crazytalk, keypad, listening, orientationcube]
    __listR = [morsecode, wires, twobits, button, colourflash, roundkeypad]
    
    def __init__(self):
        '''
        Initialize a new turnthekeys instance
        '''
        pass
    
    def solve(self, solved_instance):
        '''
        Remove the solved module from the requirement list

        Args:
            solved_instance (class): The class of a module that has just been solved
        '''
        if isinstance(solved_instance, password): self.__listL.pop(self.__listL.index(password))
        elif isinstance(solved_instance, whosonfirst): self.__listL.pop(self.__listL.index(whosonfirst))
        elif isinstance(solved_instance, crazytalk): self.__listL.pop(self.__listL.index(crazytalk))
        elif isinstance(solved_instance, keypad): self.__listL.pop(self.__listL.index(keypad))
        elif isinstance(solved_instance, listening): self.__listL.pop(self.__listL.index(listening))
        elif isinstance(solved_instance, orientationcube): self.__listL.pop(self.__listL.index(orientationcube))
        elif isinstance(solved_instance, morsecode): self.__listR.pop(self.__listR.index(morsecode))
        elif isinstance(solved_instance, wires): self.__listR.pop(self.__listR.index(wires))
        elif isinstance(solved_instance, twobits): self.__listR.pop(self.__listR.index(twobits))
        elif isinstance(solved_instance, button): self.__listR.pop(self.__listR.index(button))
        elif isinstance(solved_instance, colourflash): self.__listR.pop(self.__listR.index(colourflash))
        elif isinstance(solved_instance, roundkeypad): self.__listR.pop(self.__listR.index(roundkeypad))

    def showModules(self):
        '''
        Show the required modules left to solve

        Returns:
            tuple (list, list): Index 0 represents the required modules left to turn the left key, index 1 represents the required modules left to turn the right key
        '''
        return tuple([self.__listL, self.__listR])