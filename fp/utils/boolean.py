from fp.utils.fp import curry, flow

def isNone(arg):
    return arg is None

def toBool(arg):
    return arg != None and arg != 0 and arg != False

def flipBool(arg):
    return not arg

def negate(fn):
    return flow(
        fn,
        toBool,
        flipBool,
    )

@curry
def eq(left, right):
    return left == right

@curry
def ifElse(onTrue, onFalse, condition): 
    return lambda arg: onTrue(arg) if condition(arg) else onFalse(arg)

