from functools import wraps

import fp
from game.utils import getCoordinatesInBetween, flattenPossibleMoves, getPossibleMovesWithDestroyablePawns, isSameMove, hasQueen, isSameCoord

def moveValidator(errorMsg):
  def decorator(fn):
    @wraps(fn)
    def wrapper(dependencies, move):
      return fn(dependencies, move).chain(lambda isValid: move if isValid else fp.Left(errorMsg))
    return wrapper
  return decorator

def either(conditionA, conditionB):
  def handleMove(move):
    resultA = conditionA(move)

    if resultA:
      return resultA

    resultB = conditionB(move)

    if resultB:
      return resultB

    return fp.Left(f"{resultA.value} or {resultB.value}")
  return lambda mv: mv.chain(lambda _: handleMove(mv))

@fp.curry
def getCell(cell, dependencies, move):
  return fp.prop(dependencies["keyEncoder"](move[cell]), move["board"])

getFromCell = getCell("from")
getToCell = getCell("to")

@fp.curry
def getCellsInBetween(dependencies, move):
  return fp.filter(fp.negate(fp.isNone), getCoordinatesInBetween(move["from"], move["to"]).map(fp.flow(
    lambda coords: fp.prop(dependencies["keyEncoder"](coords), move["board"]),
    fp.value
  )))

@fp.curry
def getAllCellsOfPlayer(owner, board):
  return fp.flow(
    fp.values,
    fp.filter(fp.flow(
      fp.prop("pawn"),
      fp.chain(fp.prop("owner")),
      fp.map(fp.compareProp("id", owner)),
      fp.value
    )),
  )(board)

@fp.curry
def cellHasOwner(owner, cell):
  return fp.flow(
    fp.prop("pawn"),
    fp.chain(fp.flow(
      fp.prop("owner"),
      fp.chain(fp.compareProp("id", owner)),
    )),
  )(cell)

@fp.curry
def cellHasEnemyPawn(player, cell):
  return fp.flow(
    fp.prop("pawn"),
    fp.chain(fp.flow(
      fp.prop("owner"),
      fp.chain(lambda owner: not fp.isNone(owner) and not fp.compareProp("id", owner, player)),
    )),
  )(cell)

@fp.curry
def makeJumpsOverAvailableEnemyPawn(otherValidations):

  @fp.curry
  @moveValidator("has to jump over enemy pawn if available")
  def validationFn(dependencies, mv):
    def mapMove(move):
      movesJumpingOverEnemy = getAllCellsOfPlayer(move["player"], move["board"]).map(fp.flow(
        lambda cell: getPossibleMovesWithDestroyablePawns(
          dependencies,
          fp.flow(fp.Right.of, otherValidations),
          move["board"],
          move["player"],
          cell["at"]
        ),
        flattenPossibleMoves,
      )).join()

      if fp.isEmpty(movesJumpingOverEnemy):
        return True

      return fp.some(isSameMove(move),  movesJumpingOverEnemy)
    return mv.map(mapMove)
  return validationFn

@fp.curry
def movesBy(distance, dependencies, mv):
  return mv.map(lambda move: abs(move["from"]["x"] - move["to"]["x"]) == distance and abs(move["from"]["y"] - move["to"]["y"]) == distance)

@fp.curry
@moveValidator("has to end be within the board")
def movesWithinBoard(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move) and getToCell(dependencies, move))

@fp.curry
@moveValidator("has to have different start and end coordinates")
def movesToOtherCell(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(fp.flow(
    lambda cell: getToCell(dependencies, move).map(fp.flow(fp.eq(cell), fp.flipBool)),
    fp.value
  )))

@fp.curry
@moveValidator("has to move a pawn")
def pawnExists(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.chain(fp.negate(fp.isNone))
  )))

@fp.curry
@moveValidator("has to end on an empty tile")
def movesToEmptySpace(dependencies, mv):
  return mv.map(lambda move: getToCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.flipBool
  )))

@fp.curry
@moveValidator("has to move pawn owned by the player")
def userOwnsPawn(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(cellHasOwner(move["player"])))

@fp.curry
@moveValidator("has to move pawn diagonally")
def movesDiagonally(dependencies, mv):
  return mv.map(lambda move: abs(move["from"]["x"] - move["to"]["x"]) == abs(move["from"]["y"] - move["to"]["y"]))

@fp.curry
@moveValidator("has to not jump over own pawns")
def doesNotJumpOverSelf(dependencies, mv):
  return mv.map(fp.flow(
    lambda move: fp.some(cellHasOwner(move["player"]), getCellsInBetween(dependencies, move)),
    fp.flipBool
  ))

@fp.curry
@moveValidator("has to move forward")
def movesForward(dependencies, mv):
  return mv.map(lambda move: (move["to"]["y"] - move["from"]["y"]) * move["player"]["direction"] > 0)

@fp.curry
@moveValidator("has to land after enemy's pawn")
def landsAfterEnemyPawn(dependencies, mv):
  return mv.map(lambda move: fp.last(getCellsInBetween(dependencies, move)).chain(
    cellHasEnemyPawn(move["player"])
  ))

@fp.curry
@moveValidator("has to jump over at most 1 enemy pawn")
def jumpsOverOneEnemyPawn(dependencies, mv):
  return mv.map(lambda move: len(fp.filter(cellHasEnemyPawn(move["player"]), getCellsInBetween(dependencies, move))) == 1)

@fp.curry
@moveValidator("has to not jump over any pawn")
def doesNotJumpOverAnyPawn(dependencies, mv):
  return mv.map(lambda move: fp.every(fp.flow(fp.prop("pawn"), fp.map(fp.isNone), fp.value), getCellsInBetween(dependencies, move)))

@fp.curry
@moveValidator("has to continue previous move")
def continuesPreviousMove(dependencies, mv):
  return mv.map(lambda move: fp.isNone(move["needsToContinueMoveFrom"]) or isSameCoord(move["needsToContinueMoveFrom"], move["from"]))

movesByOneCell = fp.flow(
  moveValidator("has to move by one cell"),
  fp.curry
)(movesBy(1))

movesByTwoCells = fp.flow(
  moveValidator("has to move by two cells"),
  fp.curry
)(movesBy(2))

@fp.curry
def sharedValidation(dependencies):
  return fp.flow(
    pawnExists(dependencies),
    userOwnsPawn(dependencies),
    movesWithinBoard(dependencies),
    movesToOtherCell(dependencies),
    movesToEmptySpace(dependencies),
    movesDiagonally(dependencies),
    doesNotJumpOverSelf(dependencies),
    continuesPreviousMove(dependencies)
  )

@fp.curry
def queenValidation(dependencies):
  return fp.flow(
    sharedValidation(dependencies),
    either(
      fp.flow(landsAfterEnemyPawn(dependencies), jumpsOverOneEnemyPawn(dependencies)),
      doesNotJumpOverAnyPawn(dependencies)
    )
  )

@fp.curry
def pawnValidation(dependencies):
  return fp.flow(
    sharedValidation(dependencies),
    either(
      fp.flow(landsAfterEnemyPawn(dependencies), jumpsOverOneEnemyPawn(dependencies), movesByTwoCells(dependencies)),
      fp.flow(movesForward(dependencies), movesByOneCell(dependencies))
    )
  )

@fp.curry
def validate(dependencies, mv):
  validatingFn = fp.flow(
    fp.map(lambda move: (queenValidation if hasQueen(move["board"], dependencies["keyEncoder"](move["from"])) else pawnValidation)(dependencies)),
    fp.value
  )(mv)

  return validatingFn(mv)

@fp.curry
def validatePlayerMove(dependencies, move):
  jumpsOverAvailableEnemyPawn = makeJumpsOverAvailableEnemyPawn(validate(dependencies))

  return fp.flow(
    validate(dependencies),
    jumpsOverAvailableEnemyPawn(dependencies),
  )(fp.Right.of(move))
