import fp

from game.types import Coordinates

@fp.curry
def getCoordinatesInBetween(fromCoords, toCoords):
  [xFrom, xTo] = [fromCoords["x"], toCoords["x"]]
  [yFrom, yTo] = [fromCoords["y"], toCoords["y"]]

  [xStart, xEnd] = [xFrom, xTo] if xFrom < xTo else [xTo, xFrom]
  [yStart, yEnd] = [yFrom, yTo] if yFrom < yTo else [yTo, yFrom]

  return fp.fillWithIndex(xEnd - xStart - 1).map(fp.flow(
    fp.add(1),
    lambda offset: Coordinates(xStart + offset, yStart + offset),
  ))
