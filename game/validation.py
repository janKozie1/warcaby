from functools import wraps

import fp
from game.utils import getCoordinatesInBetween

def moveValidator(errorMsg):
  def decorator(fn):
    @wraps(fn)
    def wrapper(dependencies, move):
      return fn(dependencies, move).chain(lambda isValid: move if isValid else fp.Left(errorMsg))
    return wrapper
  return decorator

def either(conditionA, conditionB):
  # TODO: join the errors
  return lambda move: conditionA(move) or conditionB(move)

@fp.curry
def getCell(cell, dependencies, move):
  return fp.prop(dependencies["keyEncoder"](move[cell]), dependencies["board"])

getFromCell = getCell("from")
getToCell = getCell("to")

@fp.curry
def getCellsInBetween(dependencies, move):
  return fp.filter(fp.negate(fp.isNone), getCoordinatesInBetween(move["from"], move["to"]).map(fp.flow(
    lambda coords: fp.prop(dependencies["keyEncoder"](coords), dependencies["board"]),
    fp.value
  )))

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
@moveValidator("Move is not within the board")
def movesWithinBoard(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move) and getToCell(dependencies, move))

@fp.curry
@moveValidator("Start and end coordinates have to be different")
def movesToOtherCell(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(fp.flow(
    lambda cell: getToCell(dependencies, move).map(fp.flow(fp.eq(cell), fp.flipBool)),
    fp.value
  )))

@fp.curry
@moveValidator("No pawn to move")
def pawnExists(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.chain(fp.negate(fp.isNone))
  )))

@fp.curry
@moveValidator("Target tile is not empty")
def movesToEmptySpace(dependencies, mv):
  return mv.map(lambda move: getToCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.flipBool
  )))

@fp.curry
@moveValidator("Pawn does not belong to the current user")
def userOwnsPawn(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move).chain(cellHasOwner(move["player"])))

@fp.curry
@moveValidator("Pawn is not being moved diagonally")
def movesDiagonally(dependencies, mv):
  return mv.map(lambda move: abs(move["from"]["x"] - move["to"]["x"]) == abs(move["from"]["y"] - move["to"]["y"]))

@fp.curry
@moveValidator("Cannot jump over pawns of the same user")
def doesNotJumpOverSelf(dependencies, mv):
  return mv.map(fp.flow(
    lambda move: fp.some(cellHasOwner(move["player"]), getCellsInBetween(dependencies, move)),
    fp.flipBool   
  ))

@fp.curry
@moveValidator("Cannot move by more than one cell")
def movesByOneCell(dependencies, mv):
  return mv.map(lambda move: abs(move["from"]["x"] - move["to"]["x"]) == 1 and abs(move["from"]["y"] - move["to"]["y"]) == 1)

@fp.curry
@moveValidator("Pawn has to move forward")
def movesForward(dependencies, mv):
  pass

@fp.curry
@moveValidator("Has to end move after other's player pawn")
def landsAfterEnemyPawn(dependencies, mv):
  pass

@fp.curry
@moveValidator("Cannot jump over more than 1 enemy pawn")
def jumpsOverOneEnemyPawn(dependencies, mv):
  pass

@fp.curry
def validatePlayerMove(dependencies, move): 
  return fp.flow(
    movesWithinBoard(dependencies),
    movesToOtherCell(dependencies),
    pawnExists(dependencies),
    movesToEmptySpace(dependencies),
    userOwnsPawn(dependencies),
    movesDiagonally(dependencies),
    doesNotJumpOverSelf(dependencies),
    either(
      fp.flow(jumpsOverOneEnemyPawn(dependencies), landsAfterEnemyPawn(dependencies)),
      fp.flow(movesByOneCell(dependencies), movesForward(dependencies))
    )
  )(fp.Right.of(move))