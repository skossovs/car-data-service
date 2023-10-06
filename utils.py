
def left(aString, howMany):
    if howMany <1:
        return ''
    else:
        return aString[:howMany]

def right(aString, howMany):
    if howMany <1:
        return ''
    else:
        return aString[-howMany:]

def mid(aString, startChar, howMany):
    if howMany < 1:
        return ''
    else:
        return aString[startChar:startChar+howMany]