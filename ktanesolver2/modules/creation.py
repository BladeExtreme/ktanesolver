from ..edgework import edgework

class creation(edgework):
    __targettable = [
        ['bird','dinosaur','turtle','lizard','word'],
        ['ghost','plankton','seed','mushroom']
    ]
    __combinations = {
        'energy': ['fire', 'air'],
        'swamp': ['earth', 'water'],
        'life': ['swamp', 'energy'],
        'bacteria': ['life', 'swamp'],
        'plankton': ['bacteria', 'water'],
        'worm': ['bacteria', 'swamp'],
        'mushroom': ['weeds', 'earth'],
        'weeds': ['life', 'water'],
        'egg': ['life', 'earth'],
        'bird': ['egg', 'air'],
        'dinosaur': ['egg','earth'],
        'turtle': ['egg','water'],
        'lizard': ['swamp','earth'],
        'seed': ['egg','weeds'],
        'ghost': ['energy','fire']
    }
    def __check(self, w, b):
        if not isinstance(w, str): raise TypeError("weather must be in str")
        elif w not in ['sunny', 'heat', 'clear', 'rainy', 'meteor']: raise ValueError("Accepting weather value are only: 'sunny', 'heat', 'clear', 'rainy' or 'meteor'")
        elif not isinstance(b, list) and not isinstance(b, dict): raise TypeError("button must be either list or dict")
        elif len(b)!=4: raise IndexError("Length of button must be 4")
        if isinstance(b, dict):
            if not all([a.lower() in ['tl','tr','bl','br'] for a in b]): raise KeyError("Key of button must consist of: 'tl', 'tr', 'bl', 'br'")
            if not all([a.lower() in ['fire','water','air','earth'] for a in b.values()]): raise ValueError("Value of button must either be 'fire','water','air','earth'")
            elif not all([isinstance(a, str) for a in b.values()]): raise TypeError("Value of each key must be in str")
            b = [b['tl'], b['tr'], b['bl'], b['br']]
        elif isinstance(b, list):
            if not all([isinstance(a, str) for a in b]): raise TypeError("Type of button's element must be in str")
            elif not all([a.lower() in ['fire','water','air','earth'] for a in b]): raise ValueError("Value of button must either be 'fire','water','air','earth'")
        return w.lower(), [a.lower() for a in b]

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
    
    def __calculate(self):
        tableoffset = {
            'rainy': [2,1,4,3], 'windy': [1,2,3,4],
            'heat': [3,4,2,1], 'meteor': [4,3,1,2],
            'sunny': [0,0,0,0]
        }
        weatherset = {'rainy': 'water', 'heat': 'fire', 'meteor': 'earth', 'windy': 'air', 'sunny': 'fire'}
        weatheroffset = tableoffset[self.__weather][self.__button.index(weatherset[self.__weather])]

        if self.hold >= 3:
            if (len(self._litind) == len(self.ind)) and (self.batt-self.hold == 0): offset = 0
            elif len(self._litind) == len(self.ind): offset = 1
            elif len(self._unlitind) == len(self.ind) and (self.batt == self.hold): offset = 2
            elif len(self._unlitind) == len(self.ind): offset = 3
            else: offset = 4
        elif self.hold < 3:
            if len(self.ports) > self.hold: offset = 0
            elif len([a for b in self.ports for a in b]) != len(self._uniqueports): offset = 1
            elif len(self._unlitind) > len(self._litind): offset = 2
            else: offset = 3
        
        target = self.__targettable[0 if self.hold>=3 else 1][(weatheroffset+offset)%4]
        ans = []; recipes = []; idx = -1

        while not (all([a in ['energy', 'life'] for a in ans]) and len(recipes)>0):
            if target in ['water','earth','fire','air']:
                try:
                    idx+=1; target = recipes[idx]; continue
                except:
                    break
            ans.insert(0, {target: self.__combinations[target]})
            for a in self.__combinations[target]:
                if a not in recipes: recipes.append(a)
            idx+=1; target = recipes[idx]
        return tuple(ans)
        

    def solve(self):
        '''
        Solve the Creation module

        Returns:
            list (dict): The recipes to create the target creature. It is ordered from the earliest possible combination (with base elements) to the final combination (with more advanced elements)
        '''
        return self.__calculate()