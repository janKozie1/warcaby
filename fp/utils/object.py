from fp.utils.fp import curry, flow, map, value
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
