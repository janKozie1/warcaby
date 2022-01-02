import fp
from functools import reduce

from game.utils import getCoordinatesInBetween, pawnWasRemoved, getPossibleMovesWithDestroyablePawns, flattenPossibleMoves

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

  canJumpOverMore = lambda: fp.flow(
    flattenPossibleMoves,
    fp.some(fp.negate(fp.isEmpty))
  )(getPossibleMovesWithDestroyablePawns(dependencies, validate, updatedBoard, playerMove["player"], playerMove["to"]))

  return dependencies["resultCreator"](
    updatedBoard,
    playerMove["to"] if pawnWasRemoved(playerMove["board"], updatedBoard) and canJumpOverMore() else None,
    None
  )
