from abc import ABC, abstractmethod

class UI(ABC):

  @abstractmethod
  def render(self):
    pass

  @abstractmethod
  def makeMove(self, coordinates):
    pass


  
