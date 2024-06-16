from ..edgework import edgework

class creation(edgework):
    def __check(self, w, b):
        if not isinstance(w, str): raise TypeError("weather must be in str")
        elif w not in ['sunny', 'heat', 'clear', 'rainy', 'meteor']: raise ValueError("Accepting weather value are only: 'sunny', 'heat', 'clear', 'rainy' or 'meteor'")
        if not isinstance(b, list) and not isinstance(b, dict): raise TypeError("button must be either list or dict")
        if isinstance(b, dict):
            if len(b)!=4: raise IndexError("Length of button must be 4")

    def __init__(self, edgework:edgework, weather:str, button:list|dict):
        '''
        Initialize a new creation instance

        Args:
            edgework (edgework): The edgework of the bomb
            weather (str): The current weather in day 1
            button (list (str) | dict): The button list that appears on the module in reading order. In list, index 0 represents top left and index 3 represents bottom left. In dict, the accepting keys are only: 'tl', 'tr', 'bl', 'br.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__weather, self.__button = self.__check(weather.lower(), button)