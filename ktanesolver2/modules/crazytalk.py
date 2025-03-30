import re
from ..edgework import edgework

class crazytalk(edgework):
    __bank = {
	"..": "85", ".PERIOD": "81", ".STOP": "78", "<-": "63", "<- <- -> <- -> ->": "54", "<- <- RIGHT LEFT -> ->": "61", "<- LEFT -> LEFT -> RIGHT": "56", "1 3 2 4": "32", "1 3 2 FOR": "10",
    "1 3 TO 4": "30", "1 3 TOO 4": "20", "1 3 TOO WITH 2 OHS FOUR": "42", "1 3 TOO WITH TWO OS 4": "41", "1 THREE TWO FOUR": "36", "AFTER I SAY BEEP FIND THIS PHRASE WORD FOR WORD BEEP AN ACTUAL LEFT ARROW": "72", "ALL WORDS ONE THREE TO FOR FOR AS IN THIS IS FOR YOU": "40", "AN ACTUAL LEFT ARROW": "62", "AN ACTUAL LEFT ARROW LITERAL PHRASE": "53", "BLANK": "13",
    "DISREGARD WHAT I JUST SAID. FOUR WORDS, NO PUNCTUATION. ONE THREE 2 4.": "31", "DISREGARD WHAT I JUST SAID. TWO WORDS THEN TWO DIGITS. ONE THREE 2 4.": "08", "DOT DOT": "86", "EMPTY SPACE": "16", "FIVE WORDS THREE WORDS THE PUNCTUATION FULLSTOP": "19", "FOR THE LOVE OF - THE DISPLAY JUST CHANGED, I DIDN'T KNOW THIS MOD COULD DO THAT. DOES IT MENTION THAT IN THE MANUAL?": "87", "FOR THE LOVE OF ALL THAT IS GOOD AND HOLY PLEASE FULLSTOP FULLSTOP.": "90", "FULLSTOP FULLSTOP": "84", "HOLD ON CRAZY TALK WHILE I DO THIS NEEDY": "21", "HOLD ON IT'S BLANK": "19",
    "IT LITERALLY SAYS THE WORD ONE AND THEN THE NUMBERS 2 3 4": "45", "IT'S SHOWING NOTHING": "23", "LEFT": "69", "LEFT ARROW": "68", "LEFT ARROW LEFT WORD RIGHT ARROW LEFT WORD RIGHT ARROW RIGHT WORD": "58", "LEFT ARROW SYMBOL": "64", "LEFT ARROW SYMBOL TWICE THEN THE WORDS RIGHT LEFT RIGHT THEN A RIGHT ARROW SYMBOL": "59", "LEFT LEFT RIGHT <- RIGHT ->": "57", "LEFT LEFT RIGHT LEFT RIGHT RIGHT": "67", "LIMA ECHO FOXTROT TANGO SPACE ALPHA ROMEO ROMEO OSCAR RISKY SPACE SIERRA YANKEE MIKE BRAVO OSCAR LIMA": "12", "LIMA ECHO FOXTROT TANGO SPACE ALPHA ROMEO ROMEO OSCAR WHISKEY SPACE SIERRA YANKEE MIKE BRAVO OSCAR LIMA": "65",
    "LITERALLY BLANK": "15", "LITERALLY NOTHING": "14", "NO COMMA LITERALLY NOTHING": "24", "NO REALLY STOP": "51", "NO REALLY.": "52", "NO, LITERALLY NOTHING": "25", "NOTHING": "12", "NOVEBMER OSCAR SPACE, LIMA INDIA TANGO ECHO ROMEO ALPHA LIMA LIMA YANKEE SPACE NOVEMBER OSCAR TANGO HOTEL INDIA NOVEMBER GOLF": "07", "NOVEBMER OSCAR SPACE, LIMA INDIGO TANGO ECHO ROMEO ALPHA LIMA LIMA YANKEE SPACE NOVEMBER OSCAR TANGO HOTEL INDEGO NOVEMBER GOLF": "29", "OK WORD FOR WORD LEFT ARROW SYMBOL TWICE THEN THE WORDS RIGHT LEFT RIGHT THEN A RIGHT ARROW SYMBOL": "60", "ONE 3 2 4": "34", "ONE 3 2 FOUR": "38", "ONE AND THEN 3 TO 4": "47",
    "ONE IN LETTERS 3 2 4 IN NUMBERS": "35", "ONE THREE 2 WITH TWO OHS 4": "43", "ONE THREE TO FOR": "39", "ONE THREE TWO FOUR": "37", "ONE WORD THEN PUNCTUATION. STOP STOP.": "09", "PERIOD": "79", "PERIOD PERIOD": "82", "PERIOD TWICE": "83", "RIGHT ALL IN WORDS STARTING NOW ONE TWO THREE FOUR": "49", "SEVEN WORDS FIVE WORDS THREE WORDS THE PUNCTUATION FULLSTOP": "05", "STOP DOT PERIOD": "50",
    "STOP STOP": "75", "STOP TWICE": "76", "STOP.": "74", "THAT'S WHAT IT'S SHOWING": "21", "THE FOLLOWING SENTENCE THE WORD NOTHING": "27", "THE PHRASE THE WORD LEFT": "71", "THE PHRASE THE WORD NOTHING": "26", "THE PHRASE THE WORD STOP TWICE": "91", "THE PHRASE: THE PUNCTUATION FULLSTOP": "93", "THE PUNCTUATION FULLSTOP": "92",
    "THE WORD BLANK": "01", "THE WORD LEFT": "70", "THE WORD ONE AND THEN THE NUMBERS 3 2 4": "48", "THE WORD STOP TWICE": "94", "THERE ARE THREE WORDS NO PUNCTUATION READY? STOP DOT PERIOD": "50", "THERE'S NOTHING": "18", "THIS ONE IS ALL ARROW SYMBOLS NO WORDS": "28", "THREE WORDS THE PUNCTUATION FULLSTOP": "99", "THREE WORDS THE WORD STOP": "73", "WAIT FORGET EVERYTHING I JUST SAID, TWO WORDS THEN TWO SYMBOLS THEN TWO WORDS: <- <- RIGHT LEFT -> ->": "16", "WE JUST BLEW UP": "42"
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
        self.__word = self.__check(word.upper())
    
    def solve(self):
        '''
        Solve the Crazy Talk module

        Returns:
            Tuple (list [str, int, int]): The confirmed sentence and the last second digit to flick the level. Lists represents all possible answers given by word parameter. Index 0 of sub-list shows the confirmed sentence, Index 1 is the first flick, index 2 is the second flick
        '''
        ans = []
        for a in self.__bank:
            if bool(re.search(self.__word, a)):
                ans.append([a, self.__bank[a][0], self.__bank[a][1]])
        return tuple(ans)