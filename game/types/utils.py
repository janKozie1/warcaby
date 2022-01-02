import fp
from functools import wraps

@fp.curry
def makeTypeCreator(typenameKey, typename):
  def decorator(fn):

    @wraps(fn)
    def wrapper(*args):
      return fp.merge(fn(*args), fp.setProp(typenameKey, typename, {}))

    return wrapper
  return decorator

@fp.curry
def makeIsTypeOf(typenameKey, typename, obj):
  return fp.flow(
    fp.prop(typenameKey),
    fp.map(fp.eq(typename)),
    fp.value
  )(obj)

typeCreator = makeTypeCreator("__typename")
isTypeOf = makeIsTypeOf("__typename")
