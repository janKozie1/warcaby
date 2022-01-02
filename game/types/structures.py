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
def Move(player, board, fromCoordinates, toCoordinates, needsToContinueMoveFrom):
  return {
    "player": player,
    "from": fromCoordinates,
    "to": toCoordinates,
    "board": board,
    "needsToContinueMoveFrom": needsToContinueMoveFrom
  }

MoveDependenciesTypename = "MoveDependencies"
@typeCreator(MoveDependenciesTypename)
def MoveDependencies(keyEncoder, keyDecoder, resultCreator):
  return {
    "keyEncoder": keyEncoder,
    "keyDecoder": keyDecoder,
    "resultCreator": resultCreator,
  }

MoveResultTypename = "MoveResult"
@typeCreator(MoveResultTypename)
def MoveResult(board, needsToContinueMoveFrom, winner):
  return {
    "board": board,
    "needsToContinueMoveFrom": needsToContinueMoveFrom,
    "winner": winner
  }

DirectionsTypename = "Directions"
@typeCreator(DirectionsTypename)
def Directions():
  return {
    "down": 1,
    "up": -1,
  }

PossibleMovesTypename = "PossibleMoves"
@typeCreator(PossibleMovesTypename)
def PossibleMoves(topLeft, topRight, bottomLeft, bottomRight):
  return {
    "topLeft": topLeft,
    "topRight": topRight,
    "bottomLeft": bottomLeft,
    "bottomRight": bottomRight,
  }

WinnerTypename = "Winner"
@typeCreator(WinnerTypename)
def Winner(player):
  return {
    "player": player
  }