from ..edgework import edgework

class crazytalk(edgework):
    __bank = {
	"..": "85", ".period": "81", ".stop": "78",	"<-": "63",	"<- <- -> <- -> ->": "54",	"<- <- right left -> ->": "61",	"<- left -> left -> right": "56",	"1 3 2 4": "32",
	"1 3 2 for": "10",	"1 3 to 4": "30",	"1 3 too 4": "20",	"1 3 too with 2": "42",	"1 3 too with two": "41",	"1 three two four": "36",	"after i say beep find this": "72",
	"all words one three to": "40",	"an actual left arrow": "62",	"an actual left arrow literal": "53",	"blank": "13",	"disregard what i just said four": "31",	"disregard what i just said two": "08",
	"dot dot": "86",	"empty space": "16",	"five words three words the": "19",	"for the love of the": "87",	"for the love of all": "90",	"fullstop fullstop": "84",
	"hold on crazy talk while": "21",	"hold on it's blank": "19",	"it literally says the word": "45",	"it's showing nothing": "23",	"left": "69","left arrow": "68",	"left arrow left word right": "58",	"left arrow symbol": "64",	"left arrow symbol twice then": "59",	"left left right <- right": "57",	"left left right left right": "67",
	"literally blank": "15",	"literally nothing": "14",	"no comma literally nothing": "24",	"no really stop": "51",	"no really": "52",	"no, literally nothing": "25",
	"nothing": "12",	"novebmer oscar space, lima india": "07",	"novebmer oscar space, lima indigo": "29",	"ok word for word left arrow symbol": "60",	"one 3 2 4": "34",	"one 3 2 four": "38",
	"one and then 3 to": "47",	"one in letters 3 2": "35",	"one three 2 with two": "43",	"one three to for": "39",	"one three two four": "37",	"one word then punctuation stop": "09",	"period": "79",
	"period period": "82",	"period twice": "83",	"right all in words starting": "49",	"seven words five words three": "05",	"stop dot period": "50",	"stop stop": "75",	"stop twice": "76",
	"stop": "74",	"that's what it's showing": "21",	"the following sentence the word": "27",	"the phrase the word left": "71",	"the phrase the word nothing": "26",	"the phrase the word stop": "91",	"the phrase: the punctuation fullstop": "93",
	"the punctuation fullstop": "92",	"the word blank": "01",	"the word left": "70",	"the word one and then": "48",	"the word stop twice": "94",	"there are three words no": "50",
	"there's nothing": "18",	"this one is all arrow": "28",	"three words the punctuation fullstop": "99",	"three words the word stop": "73",	"wait forget everything i just": "16",	"we just blew up": "42"
    }

    def __check(self, w):
        if not isinstance(w, str): raise TypeError("Word has an invalid type")
        else: return w
    
    def __init__(self, edgework:edgework, word:str):
        '''
        Initialize a new crazytalk instance

        Args:
            edgework (edgework): The edgework of the bomb
            word (str): The word that appears on the module. Use symbols, arrows uses minus sign. (Example: "<-", "1 3 2 4")
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__word = self.__check(word.lower())
    
    def solve(self):
        '''
        Solve the Crazy Talk module

        Returns:
            Tuple (int, int): The last second digit to flick the level. Index 0 is the first flick, index 1 is the second flick
        
        Raises:
            ValueError: If no word cannot be found in the word bank
        '''
        try:
            ans = self.__bank[self.__word]
            return tuple([int(ans[0]), int(ans[1])])
        except:
            raise ValueError("Word cannot be found! Make sure to include any symbols. Arrows represented with single line (-> or <-)")