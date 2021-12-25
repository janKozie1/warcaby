class Maybe:
  def __init__(self, value):
    self.value = value
  
  def __isNothing(self):
    return self.value == None
  
  def map(self, fn):
    return self if self.__isNothing() else Maybe.of(fn(self.value))
  
  def ap(self, functor):
    return self if self.__isNothing() else functor.map(self.value)
  
  def chain(self, fn):
    return self.map(fn).join()
  
  def join(self):
    return self if self.__isNothing() else self.value

  def __bool__(self):
    return not self.__isNothing()

  def __repr__(self):
    return f"Maybe({self.value})"

  def __str__(self):
    return f"Nothing" if self.__isNothing() else f"Just({self.value})"

  @staticmethod  
  def of(value):
    return Maybe(value)