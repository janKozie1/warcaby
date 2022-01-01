import fp

from game.types import Coordinates, QueenPawnTypename, PawnTypename, isTypeOf

def determineDirection(numberA, numberB):
  return -1 if numberA > numberB else 1

@fp.curry
def getCoordinatesInBetween(fromCoords, toCoords):
  def createCoords(offset):
    xDir = determineDirection(fromCoords["x"], toCoords["x"])
    yDir = determineDirection(fromCoords["y"], toCoords["y"])

    return Coordinates(fromCoords["x"] + (offset * xDir), fromCoords["y"] + (offset * yDir))

  return fp.fillWithIndex(abs(fromCoords["x"] - toCoords["x"]) - 1).map(fp.flow(fp.add(1), createCoords))


isQueen = isTypeOf(QueenPawnTypename)
isPawn = isTypeOf(PawnTypename)
