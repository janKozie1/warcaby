from fp.utils.fp import curry, flow, map
from fp.utils.boolean import eq
from fp.functors import Maybe

@curry
def merge(dictA, dictB):
  return { **dictA, **dictB }

@curry
def prop(propKey, dictA):
  print(propKey, dictA)
  return Maybe.of(dictA[propKey]) if propKey in dictA else Maybe.of(None)

@curry
def setProp(prop, value, dictA):
  cp = dictA.copy()
  cp[prop] = value

  return cp

@curry
def compareProp(propKey, dictA, dictB):
  return prop(propKey, dictA).chain(flow(
    eq,
    map(prop(propKey, dictB))
  )).value()