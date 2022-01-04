import fp
from functools import reduce

from game.types.structures import Directions, QueenPawn

from game.logic.board import getBoardHeight
from game.logic.utils import determineWinner, getCoordinatesInBetween, pawnWasRemoved, getPossibleMovesWithDestroyablePawns, flattenPossibleMoves


@fp.curry
def placeAt(dependencies, thing, board, coordinates):
  cellKey = dependencies["keyEncoder"](coordinates)
  return fp.setProp(cellKey, fp.value(fp.prop(cellKey, board).map(fp.setProp("pawn", thing))), board)

@fp.curry
def takeAt(dependencies, board, coordinates):
  return fp.value(fp.prop(dependencies["keyEncoder"](coordinates), board).chain(fp.prop("pawn")))

@fp.curry
def move(dependencies, board, coordinatesFrom, coordinatesTo):
  return placeAt(
    dependencies,
    None,
    placeAt(dependencies, takeAt(dependencies, board, coordinatesFrom), board, coordinatesTo),
    coordinatesFrom
  )

@fp.curry
def shouldTurnIntoQueen(playerMove, board):
  if playerMove["to"]["y"] == 0 and playerMove["player"]["direction"] == Directions()["up"]:
    return True

  if playerMove["to"]["y"] == (getBoardHeight(board) - 1) and playerMove["player"]["direction"] == Directions()["down"]:
    return True

  return False

@fp.curry
def turnIntoQueen(dependencies, playerMove, board):
  return placeAt(dependencies, QueenPawn(takeAt(dependencies, board, playerMove["to"])), board, playerMove["to"])

@fp.curry
def processMove(dependencies, validate, playerMove):
  updatedBoard = move(
    dependencies,
    reduce(
      placeAt(dependencies, None),
      getCoordinatesInBetween(playerMove["from"], playerMove["to"]),
      playerMove["board"],
    ),
    playerMove["from"],
    playerMove["to"],
  )

  needsToContinueMove = pawnWasRemoved(playerMove["board"], updatedBoard) and fp.flow(
    flattenPossibleMoves,
    fp.some(fp.flow(fp.call, fp.negate(fp.isEmpty)))
  )(getPossibleMovesWithDestroyablePawns(dependencies, validate, updatedBoard, playerMove["player"], playerMove["to"]))

  boardWithQueens = turnIntoQueen(dependencies, playerMove, updatedBoard) if not needsToContinueMove and shouldTurnIntoQueen(playerMove, updatedBoard) else updatedBoard

  return dependencies["resultCreator"](
    boardWithQueens,
    playerMove["to"] if needsToContinueMove else None,
    determineWinner(dependencies, validate, boardWithQueens)
  )
