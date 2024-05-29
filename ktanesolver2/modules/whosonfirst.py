from ..edgework import edgework

class whosonfirst(edgework):
    __bank = [
        ['ur'],
        ['first', 'okay', 'c'],
        ['yes', 'nothing', 'led', 'they are'],
        ['blank', 'read', 'red', 'you', 'your', "you're", 'their'],
        ['', 'reed', 'leed', "they're"],
        ['display', 'says', 'lead', 'hold on', 'you are', 'there', 'see', 'cee']
    ]
    __list = {
        "blank": ["wait", "right", "okay", "middle", "blank"],
	    "done": ["sure", "uh huh", "next", "what?", "your", "ur", "you're", "hold", "like", "you", "u", "you are", "uh uh", "done"],
	    "first": ["left", "okay", "yes", "middle", "no", "right", "nothing", "uhhh", "wait", "ready", "blank", "what", "press", "first"],
	    "hold": ["you are", "u", "done", "uh uh", "you", "ur", "sure", "what?", "you're", "next", "hold"],
	    "left": ["right", "left"],
	    "like": ["you're", "next", "u", "ur", "hold", "done", "uh uh", "what?", "uh huh", "you", "like"],
	    "middle": ["blank", "ready", "okay", "what", "nothing", "press", "no", "wait", "left", "middle"],
	    "next": ["what?", "uh huh", "uh uh", "your", "hold", "sure", "next"],
	    "no": ["blank", "uhhh", "wait", "first", "what", "ready", "right", "yes", "nothing", "left", "press", "okay", "no"],
	    "nothing":["uhhh", "right", "okay", "middle", "yes", "blank", "no", "press", "left", "what", "wait", "first", "nothing"],
	    "okay": ["middle", "no", "first", "yes", "uhhh", "nothing", "wait", "okay"],
	    "press": ["right", "middle", "yes", "ready", "press"],
	    "ready": ["yes", "okay", "what", "middle", "left", "press", "right", "blank", "ready"],
	    "right": ["yes", "nothing", "ready", "press", "no", "wait", "what", "right"],
	    "sure": ["you are", "done", "like", "you're", "you", "hold", "uh huh", "ur", "sure"],
	    "u": ["uh huh", "sure", "next", "what?", "you're", "ur", "uh uh", "done", "u"],
	    "uh uh": ["ur", "u", "you are", "you're", "next", "uh uh"],
	    "uhhh": ["ready", "nothing", "left", "what", "okay", "yes", "right", "no", "press", "blank", "uhhh"],
	    "ur": ["done", "u", "ur"],
	    "wait": ["uhhh", "no", "blank", "okay", "yes", "left", "first", "press", "what", "wait"],
	    "what": ["uhhh", "what"],
	    "what?": ["you", "hold", "you're", "your", "u", "done", "uh uh", "like", "you are", "uh huh", "ur", "next", "what?"],
	    "yes": ["okay", "right", "uhhh", "middle", "first", "what", "press", "ready", "nothing", "yes"],
	    "you are":["your", "next", "like", "uh huh", "what?", "done", "uh uh", "hold", "you", "u", "you're", "sure", "ur", "you are"],
	    "you": ["sure", "you are", "your", "you're", "next", "uh huh", "ur", "hold", "what?", "you"],
	    "your": ["uh uh", "you are", "uh huh", "your"],
	    "youre": ["you", "you're"]
    }
    
    def __check(self, d, b):
        if not isinstance(d, str): raise TypeError("Display has an invalid type")
        elif not isinstance(b, list): raise TypeError("Buttons has an invalid type")
        elif len(b) != 6: raise IndexError("Buttons' length must be 6")
        return d, b
    
    def __init__(self, edgework, display: str, buttons: list):
        '''
        Initializes a new whosonfirst instance.
        
        Args:
		 	edgework (edgework): The edgework of the bomb
            display (str): The word displayed on the module
			buttons (list [str]): The word buttons on the module
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__display, self.__buttons = self.__check(display.lower(), [a.lower() for a in buttons])
    
    def __calculate(self, p):
    	for a in self.__list[self.__buttons[p]]:
            if a in self.__buttons: return self.__buttons.index(a)

    def solve(self):
        '''
        Solve the Who's on First module
        
        Returns:
		 	(int, str): The position of the button in numbers (0-6) alongside the word of the button
        '''
        ans = self.__calculate([a for a in range(len(self.__bank)) if self.__display in self.__bank[a]][0])
        return ans, self.__buttons[ans]