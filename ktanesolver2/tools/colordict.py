__colordict = {
    'r': 'red',
    'b': 'blue',
    'g': 'green',
    'y': 'yellow',
    'o': 'orange',
    'w': 'white',
    'k': 'black',
    'c': 'cyan',
    'm': 'magenta',
    'a': 'gray',
    'p': 'purple',
    'i': 'pink'
}

def _colorcheck(a):
    if isinstance(a, list):
        for iter in range(len(a)):
            if len(a[iter]) == 1:
                try:
                    a[iter] = __colordict.get(a[iter])
                except:
                    raise ValueError("Letter cannot be found on colordict")
            else:
                if a not in [b for b in __colordict.values()]+['pink']: raise ValueError("Color cannot be found on colordict")
    elif isinstance(a, str) and len(a) == 1:
        try:
            a = __colordict.get(a)
        except:
            raise ValueError("Letter cannot be found on colordict")
    elif isinstance(a, str) and a not in [b for b in __colordict.values()]+['pink']:
        raise ValueError("Color cannot be found on colordict")
    return a
