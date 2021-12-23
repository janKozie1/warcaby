#  export const curry = (fn) => (...args) => isLess(args.length)(fn.length)
#   ? curry(bind(...args)(fn))
#   : call(...args)(fn)

from inspect import getargspec
from functools import reduce, wraps

def flow(*fns):
    return lambda arg: reduce(lambda prev_result, fn: fn(prev_result), fns, arg)

def value(func):
    return func.value

def identity(arg):
    return arg

args_len = flow(getargspec, lambda spec: spec[0], len)

def curry(fn, args = ()):
    applied_args = args

    applied_args_amount = len(applied_args)
    required_args_amount = args_len(fn)

    @wraps(fn)
    def wrapper(*args):
        if required_args_amount == len(args) + applied_args_amount:
            return fn(*(applied_args + args))
        else:
            return curry(fn, applied_args + args)

    return wrapper

@curry
def map(fn, func):
    return func.map(fn)

@curry
def chain(fn, func):
    return func.chain(fn)
        


