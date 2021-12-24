class Array(list):
  def __init__(self, *args):
    super().__init__(args)

  def map(self, fn):
    return Array(*[fn(i) for i in self])

  def chain(self, fn):
    return self.map(fn).join()

  def join(self):
    return Array(*[item for sublist in self for item in sublist])

