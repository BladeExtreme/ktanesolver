from ..edgework import edgework

class listening(edgework):
    __bank = {
        'taxi dispatch':        '&&&**',
        'cow':                  '&$#$&',
        'extractor fan':        '#$#*&',
        'train station':        '#$$**',
        'arcade':               '$#$#*',
        'casino':               '**$*#',
        'supermarket':          '#$$&*',
        'soccer match':         '##*$*',
        'tawny owl':            '$#*$&',
        'sewing machine':       '#&&*#',
        'thrush nightingale':   '**#**',
        'car engine':           '&#**&',
        'reloading glock 19':   '$&**#',
        'oboe':                 '&#$$#',
        'saxophone':            '$&&**',
        'tuba':                 '#&$##',
        'marimba':              '&*$*$',
        'phone ringing':        '&$$&*',
        'tibetan nuns':         '#&&&&',
        'throat singing':       '**$$$',
        'beach':                '*&*&&',
        'dial-up internet':     '*#&*&',
        'police radio scanner': '**###',
        'censorship bleep':     '&&$&*',
        'medieval weapons':     '&$**&',
        'door closing':         '#$#&$',
        'chainsaw':             '&#&&#',
        'compressed air':       '$$*$*',
        'servo motor':          '$&#$$',
        'waterfall':            '&**$$',
        'tearing fabric':       '$&&*&',
        'zipper':               '&$&##',
        'vacuum cleaner':       '#&$*&',
        'ballpoint pen writing':'$*$**',
        'rattling iron chain':  '*#$&&',
        'book page turning':    '###&$',
        'table tennis':         '*$$&$',
        'squeaky toy':          '$*&##',
        'helicopter':           '#&$&&',
        'firework exploding':   '$&$$*',
        'glass shattering':     '*$*$*'
    }

    def __init__(self, edgework: edgework, audio:str|None=None):
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if audio is not None:
            self.__audio = self.__check(audio.lower())
    
    def __check(self, a):
        if not isinstance(a, str): raise TypeError("Audio has an invalid type")
        elif not any([True if a == z else False for z,b in self.__bank.items()]): raise ValueError("Audio's name not found. Perhaps check with listening.showNames()?")
        return a

    def showNames(self):
        return tuple([z for z,b in self.__bank.items()])

    def solve(self):
        return self.__bank[self.__audio]