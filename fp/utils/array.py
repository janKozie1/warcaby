from fp.functors import Maybe, Array

from fp.utils.fp import flow, curry, value
from fp.utils.math import eq

isEmpty = flow(len, eq(0))

@curry
def nth(n, arr):
  return Maybe.of(arr[n]) if len(arr) > n else Maybe.of(None)

head = nth(0)
second = nth(1)

def tail(arr):
  return Maybe.of(Array(*arr[1:])) if not isEmpty(arr) else Maybe.of(None)

@curry
def fill(thing, size):
  return Array(*[thing for _ in range(0, size)])

def withIndex(arr):
  return Array(*[Array(*enum) for enum in enumerate(arr)])

def fillWithIndex(size):
  return withIndex(fill(None, size)).map(flow(head, value))



