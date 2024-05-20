__morsedict = {
    ".-": 'a',
    "-...": 'b',
    "-.-.": 'c',
    "-..": 'd',
    ".": 'e',
    "..-.": 'f',
    "--.": 'g',
    "....": 'h',
    "..": 'i',
    ".---": 'j',
    "-.-": 'k',
    ".-..": 'l',
    "--": 'm',
    "-.": 'n',
    "---": 'o',
    ".--.": 'p',
    "--.-": 'q',
    ".-.": 'r',
    "...": 's',
    "-": 't',
    "..-": 'u',
    "...-": 'v',
    ".--": 'w',
    "-..-": 'x',
    "-.--": 'y',
    "--..": 'z',
    "-----": '0',
    ".----": '1',
    "..---": '2',
    "...--": '3',
    "....-": '4',
    ".....": '5',
    "-....": '6',
    "--...": '7',
    "---..": '8',
    "----.": '9'
}

def _translate(m):
    if isinstance(m, str):
        t = __morsedict.get(m)
        if t == None: raise IndexError(f"Morse code: '{m}' is invalid")
    elif isinstance(m, list):
        t = []
        for a in range(len(m)):
            t.append(__morsedict.get(m[a]))
        if None in t: raise IndexError(f"Morse code: '{m[t.index(None)]}' is invalid")
    return t