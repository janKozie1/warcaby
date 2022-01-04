from functools import reduce

import fp

from game.types import Coordinates, PossibleMoves, Move, Winner, QueenPawnTypename, PawnTypename, isTypeOf

from game.logic.board import getBoardWidth, getBoardHeight

isQueen = isTypeOf(QueenPawnTypename)
isPawn = isTypeOf(PawnTypename)

def determineDirection(numberA, numberB):
  """determines if number should grow or lessen, to generate coordinates in order"""
  return -1 if numberA > numberB else 1

@fp.curry
def getCoordinatesInBetween(fromCoords, toCoords):
  """gets coodinates between two coordinates in order as if pawn was moving from start to end"""
  def createCoords(offset):
    xDir = determineDirection(fromCoords["x"], toCoords["x"])
    yDir = determineDirection(fromCoords["y"], toCoords["y"])

    return Coordinates(fromCoords["x"] + (offset * xDir), fromCoords["y"] + (offset * yDir))

  distance = abs(fromCoords["x"] - toCoords["x"])
  return [] if distance == 0 else fp.fillWithIndex(distance - 1).map(fp.flow(fp.add(1), createCoords))

@fp.curry
def hasQueen(board, coordinates):
  """generates every possible move for player from given coordinates, then filters the valid ones"""
  return fp.value(fp.prop(coordinates, board).chain(fp.prop("pawn")).map(isQueen))

@fp.curry
def getPossibleMoves(dependencies, validate, board, player, coordinates):
  """generates every possible move for player from given coordinates, then filters the valid ones"""
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

  return PossibleMoves(*fp.Array(topLeft, topRight, bottomLeft, bottomRight).map(lambda corner: lambda: getMoves(corner)))

@fp.curry
def getPossibleMovesWithDestroyablePawns(dependencies, validate, board, player, coordinates):
  """filters possible moves to only include the ones that remove a pawn"""
  def preceededByEnemyPawn(move):
    return fp.last(getCoordinatesInBetween(move["from"], move["to"])).map(fp.flow(
      dependencies["keyEncoder"],
      lambda coordinates: board[coordinates],
      fp.prop("pawn"),
      fp.map(lambda pawn: not fp.isNone(pawn) and not fp.compareProp("id", pawn["owner"], player)),
      fp.value
    ))

  return PossibleMoves(*flattenPossibleMoves(
    getPossibleMoves(dependencies, validate, board, player, coordinates)
  ).map(lambda getter: lambda: fp.filter(preceededByEnemyPawn, getter())))

@fp.curry
def pawnWasRemoved(previousBoard, board):
  """checks if any pawn was removed between different board states"""
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
  """checks if someone won by checking how many moves they have available"""
  cellGroups = fp.flow(
    fp.values,
    fp.filter(fp.flow(fp.prop("pawn"), fp.map(fp.negate(fp.isNone)), fp.value)),
    fp.groupBy(lambda cellWithPawn: cellWithPawn["pawn"]["owner"]["id"]),
    fp.values
  )(board)

  firstPlayerCells = fp.reverse(fp.value(fp.head(cellGroups)) or [])
  secondPlayerCells = fp.value(fp.second(cellGroups)) or []

  def anyCellHasMoves(hasMoves, cell):
    return hasMoves or fp.some(fp.flow(fp.call, fp.negate(fp.isEmpty)), flattenPossibleMoves(getPossibleMoves(
      dependencies, validate, board, cell["pawn"]["owner"], cell["at"]
    )))

  firstPlayerHasAvailableMoves = reduce(anyCellHasMoves, firstPlayerCells, False)
  secondPlayerHasAvailableMoves = reduce(anyCellHasMoves, secondPlayerCells, False)

  if firstPlayerHasAvailableMoves and secondPlayerHasAvailableMoves:
    return None

  if firstPlayerHasAvailableMoves and not secondPlayerHasAvailableMoves:
    return Winner(firstPlayerCells[0]["pawn"]["owner"])

  if not firstPlayerHasAvailableMoves and secondPlayerHasAvailableMoves:
    return Winner(secondPlayerCells[0]["pawn"]["owner"])

  return Winner(None)

@fp.curry
def flattenPossibleMoves(possibleMoves):
  return fp.Array(*[possibleMoves["topLeft"], possibleMoves["topRight"], possibleMoves["bottomLeft"], possibleMoves["bottomRight"]])

@fp.curry
def isSameCoord(coordA, coordB):
  return coordA["x"] == coordB["x"] and coordA["y"] == coordB["y"]

@fp.curry
def isSameMove(moveA, moveB):
  return isSameCoord(moveA["to"], moveB["to"]) and isSameCoord(moveA["from"], moveB["from"]) and fp.compareProp("id", moveA["player"], moveB["player"])
