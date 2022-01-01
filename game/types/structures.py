import fp

from game.types.utils import typeCreator

PlayerTypename = "Player"
@typeCreator(PlayerTypename)
def Player(id, direction):
  return {
    "id": id,
    "direction": direction,
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
  return { **pawn }

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

MoveTypename = "Move"
@typeCreator(MoveTypename)
def Move(player, board, fromCoordinates, toCoordinates):
  return {
    "player": player,
    "from": fromCoordinates,
    "to": toCoordinates,
    "board": board,
  }

MoveDependenciesTypename = "MoveDependencies"
@typeCreator(MoveDependenciesTypename)
def MoveDependencies(keyEncoder, keyDecoder):
  return {
    "keyEncoder": keyEncoder,
    "keyDecoder": keyDecoder,
  }
