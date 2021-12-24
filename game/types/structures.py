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

