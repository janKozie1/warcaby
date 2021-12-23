from fp.utils.fp import curry

@curry
def add(a, b):
  return a + b

@curry
def eq(a, b):
  return a == b