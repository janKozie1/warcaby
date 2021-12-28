class Right:
  def __init__(self, value):
    self.value = value

  def isLeft(self):
    return False
  
  def isRight(self):
    return True
  
  def map(self, fn):
    return Right.of(fn(self.value))
  
  def ap(self, func):
    return func.map(self.value)
  
  def join(self):
    return self.value
  
  def chain(self, fn):
    return self.map(fn).join()

  def __bool__(self):
    return True
  
  def __repr__(self):
    return f"Right({self.value})"

  def __str__(self):
     return f"Right({self.value})"

  @staticmethod  
  def of(value):
    return Right(value)
  
class Left:
  def __init__(self, value):
    self.value = value
  
  def isLeft(self):
    return True
  
  def isRight(self):
    return False
  
  def map(self, fn):
    return self
  
  def chain(self, func):
    return self
  
  def join(self):
    return self
  
  def ap(self, func):
    return self

  def __bool__(self):
    return False

  def __repr__(self):
    return f"Left({self.value})"

  def __str__(self):
     return f"Left({self.value})"
  

