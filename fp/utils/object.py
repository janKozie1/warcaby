from fp.utils.fp import curry
from fp.functors import Maybe

@curry
def merge(dictA, dictB):
  return { **dictA, **dictB }

@curry
def prop(prop, dictA):
  return Maybe.of(dictA[prop]) if prop in dictA else Maybe.of(None)

def setProp(prop, value, dictA):
  cp = dictA.copy()
  cp[prop] = value

  return cp