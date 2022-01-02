from functools import reduce

import fp
from game.types import Coordinates, PossibleMoves, Move, Winner, QueenPawnTypename, PawnTypename, isTypeOf
from game.board import getBoardWidth, getBoardHeight

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
def getPossibleMoves(dependencies, validate, board, player, coordinates):
  def getPlayerMv(toCoordinates):
    return Move(player, board, coordinates, toCoordinates, None)

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
def getPossibleMovesWithDestroyablePawns(dependencies, validate, board, player, coordinates):
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

@fp.curry
def pawnWasRemoved(previousBoard, board):
  def cellHasPawn(cell):
    return fp.prop("pawn", cell).map(fp.negate(fp.isNone))

  getPawnsAmount = fp.flow(
    fp.values,
    fp.filter(cellHasPawn),
    len
  )

  return getPawnsAmount(board) != getPawnsAmount(previousBoard)

@fp.curry
def determineWinner(dependencies, validate, board):
  cellGroups = fp.flow(
    fp.values,
    fp.filter(fp.flow(fp.prop("pawn"), fp.map(fp.negate(fp.isNone)), fp.value)),
    fp.groupBy(lambda cellWithPawn: cellWithPawn["pawn"]["owner"]["id"]),
    fp.values
  )(board)

  firstPlayerCells = fp.value(fp.head(cellGroups)) or []
  secondPlayerCells = fp.value(fp.second(cellGroups)) or []

  def anyCellHasMoves(hasMoves, cell):
    return hasMoves or len(getPossibleMoves(
      dependencies, validate, board, cell["pawn"]["owner"], cell["at"]
    )) != 0

  firstPlayerHasAvailableMoves = reduce(anyCellHasMoves, firstPlayerCells, False)
  secondPlayerHasAvailableMoves = reduce(anyCellHasMoves, secondPlayerCells, False)

  if firstPlayerHasAvailableMoves and secondPlayerHasAvailableMoves:
    return None

  if firstPlayerHasAvailableMoves and not secondPlayerHasAvailableMoves:
    print(firstPlayerCells[0]["pawn"]["owner"])
    return Winner(firstPlayerCells[0]["pawn"]["owner"])

  if not firstPlayerHasAvailableMoves and secondPlayerHasAvailableMoves:
    print(secondPlayerCells[0]["pawn"]["owner"])
    return Winner(secondPlayerCells[0]["pawn"]["owner"])

  return Winner(None)

@fp.curry
def flattenPossibleMoves(possibleMoves):
  return fp.Array(*[*possibleMoves["topLeft"], *possibleMoves["topRight"], *possibleMoves["bottomLeft"], *possibleMoves["bottomRight"]])

@fp.curry
def isSameCoord(coordA, coordB):
  return coordA["x"] == coordB["x"] and coordA["y"] == coordB["y"]

@fp.curry
def isSameMove(moveA, moveB):
  return isSameCoord(moveA["to"], moveB["to"]) and isSameCoord(moveA["from"], moveB["from"]) and fp.compareProp("id", moveA["player"], moveB["player"])
