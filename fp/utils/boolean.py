from fp.utils.fp import curry, flow

def isNone(arg):
    return arg is None

def toBool(arg):
    return arg != None and arg != 0 and arg != False

@curry
def eq(left, right):
    return left == right

