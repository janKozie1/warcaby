import fp

from game.types.utils import typeCreator

PlayerTypename = "Player"
@typeCreator(PlayerTypename)
def Player(id):
  return {
    "id": id
  }

PawnTypename = "Pawn"
@typeCreator(PawnTypename)
def Pawn(owner):
  return {
    "owner": owner
  }

QueenPawnTypename = "QueenPawn"
@typeCreator(QueenPawnTypename)
def QueenPawn(pawn):
  return {
    "pawn": pawn
  }

CoordinatesTypename = "Coordinates"
@typeCreator(CoordinatesTypename)
def Coordinates(x, y):
  return {
    "x": x,
    "y": y,
  }

CellTypename = "Cell"
@typeCreator(CellTypename)
def Cell(coordinates, pawn):
  return {
    "pawn": pawn,
    "at": coordinates,
  }

