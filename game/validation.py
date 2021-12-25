from functools import wraps

import fp

def moveValidator(errorMsg):
  def decorator(fn):
    @wraps(fn)
    def wrapper(dependencies, move):
      return fn(dependencies, move).chain(lambda isValid: move if isValid else fp.Left(errorMsg))
    return wrapper
  return decorator

@fp.curry
def getCell(cell, dependencies, move):
  return fp.prop(dependencies["keyEncoder"](move[cell]), dependencies["board"])

getFromCell = getCell("from")
getToCell = getCell("to")

@fp.curry
@moveValidator("Move is not within the board")
def movesWithinBoard(dependencies, mv):
  return mv.map(lambda move: getFromCell(dependencies, move) and getToCell(dependencies, move))

@fp.curry
@moveValidator("No pawn to move")
def pawnExists(dependencies, mv):
  return mv.map((lambda move: getFromCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.chain(fp.negate(fp.isNone))
  ))))

@fp.curry
@moveValidator("Target tile is not empty")
def movesToEmptySpace(dependencies, mv):
  return mv.map((lambda move: getToCell(dependencies, move).chain(fp.flow(
    fp.prop("pawn"),
    fp.flipBool
  ))))

@fp.curry
@moveValidator("Pawn does not belong to the current user")
def userOwnsPawn(dependencies, mv):
  pass

@fp.curry
@moveValidator("Pawn is not being moved diagonally")
def movesDiagonally(dependencies, mv):
  pass

@fp.curry
def validatePlayerMove(dependencies, move): 
  return fp.flow(
    movesWithinBoard(dependencies),
    movesToEmptySpace(dependencies),
    pawnExists(dependencies),
  )(fp.Right.of(move))