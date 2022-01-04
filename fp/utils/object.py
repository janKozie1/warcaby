from functools import reduce

from fp.utils.fp import curry, flow, forEach, map, value, forEach
from fp.utils.boolean import eq
from fp.functors import Maybe, Array

@curry
def merge(dictA, dictB):
  return { **dictA, **dictB }

@curry
def has(propKey, dictA):
  return propKey in dictA

@curry
def prop(propKey, dictA):
  return Maybe.of(dictA[propKey]) if has(propKey, dictA) else Maybe.of(None)

@curry
def setProp(prop, value, dictA):
  cp = dictA.copy()
  cp[prop] = value

  return cp

@curry
def values(dictA):
  return Array(*dictA.values())

@curry
def keys(dictA):
  return Array(*dictA.keys())

@curry
def compareProp(propKey, dictA, dictB):
  return value(prop(propKey, dictA).chain(lambda propValue: flow(
    prop(propKey),
    map(eq(propValue))
  )(dictB)))

@curry
def mapDict(mappingFn, dictA):
  return flow(
    keys,
    map(lambda key: { key: mappingFn(value(prop(key, dictA)), key) }),
    lambda cells: reduce(merge, cells, {})
  )(dictA)

@curry
def forEachDict(fn, dictA):
  return flow(
    keys,
    forEach(lambda key: fn(value(prop(key, dictA)), key))
  )(dictA)
