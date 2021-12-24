import fp
from game.types import Pawn, QueenPawn

@fp.curry
def areSameCoords(coordA, coordsB):
  return fp.prop("x", fp.map)

@fp.curry
def isCellAt(coords, cell):
  return cell["at"]["x"] == coords["x"] and cell["y"] == y