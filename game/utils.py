from functools import reduce

import fp
from game.types import Coordinates, PossibleMoves, Move, QueenPawnTypename, PawnTypename, isTypeOf

isQueen = isTypeOf(QueenPawnTypename)
isPawn = isTypeOf(PawnTypename)

def determineDirection(numberA, numberB):
  return -1 if numberA > numberB else 1

@fp.curry
def getCoordinatesInBetween(fromCoords, toCoords):
  def createCoords(offset):
    xDir = determineDirection(fromCoords["x"], toCoords["x"])
    yDir = determineDirection(fromCoords["y"], toCoords["y"])

    return Coordinates(fromCoords["x"] + (offset * xDir), fromCoords["y"] + (offset * yDir))

  distance = abs(fromCoords["x"] - toCoords["x"])
  return [] if distance == 0 else fp.fillWithIndex(distance - 1).map(fp.flow(fp.add(1), createCoords))

@fp.curry
def hasQueen(board, coordinates):
  return fp.value(fp.prop(coordinates, board).chain(fp.prop("pawn")).map(isQueen))

@fp.curry
def getBoardHeight(board):
  return reduce(lambda height, cell: height if cell["at"]["y"] < height else cell["at"]["y"], fp.values(board), 0)

@fp.curry
def getBoardWidth(board):
  return reduce(lambda width, cell: width if cell["at"]["x"] < width else cell["at"]["x"], fp.values(board), 0)

@fp.curry
def getPossibleMoves(dependencies, validate, board, player, coordinates):
  def getPlayerMv(toCoordinates):
    return Move(player, board, coordinates, toCoordinates)

  getMoves = fp.flow(
    lambda end: fp.Array(*getCoordinatesInBetween(coordinates, end), end),
    fp.map(getPlayerMv),
    fp.filter(validate)
  )

  maxXDistance = getBoardWidth(board) if hasQueen(board, dependencies["keyEncoder"](coordinates)) else 2
  maxYDistance = getBoardHeight(board) if hasQueen(board, dependencies["keyEncoder"](coordinates)) else 2

  topLeft = Coordinates(coordinates["x"] - maxXDistance, coordinates["y"] - maxYDistance)
  topRight = Coordinates(coordinates["x"] + maxXDistance, coordinates["y"] - maxYDistance)
  bottomLeft = Coordinates(coordinates["x"] - maxXDistance, coordinates["y"] + maxYDistance)
  bottomRight = Coordinates(coordinates["x"] + maxXDistance, coordinates["y"] + maxYDistance)

  return PossibleMoves(*fp.Array(topLeft, topRight, bottomLeft, bottomRight).map(getMoves))

@fp.curry
def getCoordinatesWithDestroyablePawns(dependencies, validate, board, player, coordinates):
  possibleMoves = getPossibleMoves(dependencies, validate, board, player, coordinates)

  topLeft = possibleMoves["topLeft"]
  topRight = possibleMoves["topRight"]
  bottomLeft = possibleMoves["bottomLeft"]
  bottomRight = possibleMoves["bottomRight"]

  def preceededByEnemyPawn(move):
    return fp.last(getCoordinatesInBetween(move["from"], move["to"])).map(fp.flow(
      dependencies["keyEncoder"],
      lambda coordinates: board[coordinates],
      fp.prop("pawn"),
      fp.map(lambda pawn: not fp.isNone(pawn) and not fp.compareProp("id", pawn["owner"], player)),
      fp.value
    ))

  return PossibleMoves(*fp.Array(topLeft, topRight, bottomLeft, bottomRight).map(fp.filter(preceededByEnemyPawn)))
  


