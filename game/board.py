import fp
from game.types import Coordinates, Cell, Pawn

@fp.curry
def keyEncoder(separator, coordinates):
  return f"{coordinates['x']}{separator}{coordinates['y']}" 

@fp.curry
def keyDecoder(separator, key):
  return fp.Array(*key.split(separator))

encodeKey = keyEncoder("-")
decodeKey = keyDecoder("-")


@fp.curry
def createBoard(width, height, mapping_fn):
  return { encodeKey(Coordinates(x, y)): mapping_fn(x, y) for y in range(0, height) for x in range(0, width) }

make8x8Board = createBoard(8, 8)
make10x10Board = createBoard(10, 10)

@fp.curry
def englishBoardPlacementRules(playerOne, playerTwo, x, y):
  cellCoordinates = Coordinates(x, y)

  if (x + y) % 2 == 1:
    if y < 3: 
      return Cell(cellCoordinates, Pawn(playerOne))
    if y > 4:
      return Cell(cellCoordinates, Pawn(playerTwo))
    
  return Cell(cellCoordinates, None)