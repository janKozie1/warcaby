from functools import reduce

from fp.functors import Maybe, Array

from fp.utils.fp import flow, curry, value
from fp.utils.boolean import eq
from fp.utils.object import setProp, prop, has

isEmpty = flow(len, eq(0))

@curry
def nth(n, arr):
  return Maybe.of(arr[n]) if len(arr) > n else Maybe.of(None)

head = nth(0)
second = nth(1)

@curry
def tail(arr):
  return Maybe.of(Array(*arr[1:])) if not isEmpty(arr) else Maybe.of(None)

@curry
def last(arr):
  return Maybe.of(arr[-1]) if not isEmpty(arr) else Maybe.of(None)

@curry
def fill(thing, size):
  return Array(*[thing for _ in range(0, size)])

@curry
def withIndex(arr):
  return Array(*[Array(*enum) for enum in enumerate(arr)])

@curry
def fillWithIndex(size):
  return withIndex(fill(None, size)).map(flow(head, value))

@curry
def append(el, arr):
  return Array(*arr, el)

@curry
def find(predicate, array):
  for el in array:
    if predicate(el):
      return Maybe.of(el)

  return Maybe.of(None)

@curry
def filter(predicate, array):
  return Array(*[el for el in array if predicate(el)])

@curry
def groupBy(predicate, array):
  def reducer(groups, el):
    dictKey = predicate(el)

    return setProp(
      dictKey,
      value(prop(dictKey, groups).map(append(el))) if has(dictKey, groups) else Array(el),
      groups
    )

  return reduce(reducer, array, {})

@curry
def sort(predicate, array):
  cp = array.copy()
  cp.sort(key = predicate)

  return cp

@curry
def some(predicate, array):
  return len(filter(predicate, array)) != 0

@curry
def every(predicate, array):
  return len(filter(predicate, array)) == len(array)

@curry
def reverse(array):
  return Array(*array[::-1])
