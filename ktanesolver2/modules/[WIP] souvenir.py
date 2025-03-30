from ..edgework import edgework
import os
import importlib

class souvenir():
    def __init__(self, edgework:edgework):
        '''
        Initialize a souvenir instance
        '''
        modules_dir = os.path.dirname(__file__)
        self.__modules = {}

        for a in os.listdir(modules_dir):
            if a.endswith(".py") and a!='souvenir.py' and a!='__init__.py':
                module_name = a[:-3]
                module = importlib.import_module(f".{module_name}", package=__package__)
                if hasattr(module, module_name):
                    class_ref = getattr(module, module_name)
                    self.__modules[module_name] = class_ref
    
    def bitmaps(self, kgrid):
        return [
            ['How many pixels were black in each quadrant?', kgrid],
            ['How many pixels were white in each quadrant?', [abs(16-a) for a in kgrid]],
        ]

    def binaryleds(self, wires):
        return [["At which numeric value did you cut the correct wire?", wires]]

    def bulb(self, string):
        return [["What were the correct button presses?", ''.join(string).replace('U','').replace('S','')]]