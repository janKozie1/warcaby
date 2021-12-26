
import fp
import game

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
  return { encodeKey(game.Coordinates(x, y)): mapping_fn(x, y) for y in range(0, height) for x in range(0, width) }

@fp.curry
def polishBoardPlacementRules(playerOne, playerTwo, x, y):
  cellCoordinates = game.Coordinates(x, y)

  if (x + y) % 2 == 1:
    if y < 4: 
      return game.Cell(cellCoordinates, game.Pawn(playerOne))
    if y > 5:
      return game.Cell(cellCoordinates, game.Pawn(playerTwo))
    
  return game.Cell(cellCoordinates, None)

@fp.curry
def placeAt(coordinates, thing, board):
  cellKey = encodeKey(coordinates)
  return fp.setProp(cellKey, fp.value(fp.prop(cellKey, board).map(fp.setProp("pawn", thing))), board)

@fp.curry
def takeAt(coordinates, board):
  return fp.value(fp.prop(encodeKey(coordinates), board).chain(fp.prop("pawn")))

@fp.curry
def move(coordinatesFrom, coordinatesTo, board):
  return fp.flow(
    placeAt(coordinatesTo, takeAt(coordinatesFrom, board)),
    placeAt(coordinatesFrom, None)
  )(board)

def cellRepr(cell):
  if cell["pawn"] is None:
    return "-"

  return  f'{cell["pawn"]["owner"]["id"]}'

def printBoard(board):
  fp.flow(
    fp.keys,
    fp.groupBy(fp.flow(decodeKey, fp.second, fp.value)),
    fp.values,
    fp.map(fp.map(lambda key: fp.value(fp.prop(key, board)))),
    fp.forEach(lambda row: print(row.map(cellRepr)))
  )(board)

playerOne = game.Player(1)
playerTwo = game.Player(2)

make10x10Board = createBoard(10, 10)
polishBoard = make10x10Board(polishBoardPlacementRules(playerOne, playerTwo))

printBoard(polishBoard)
#print(takeAt(game.Coordinates(1, 0), polishBoard))
#printBoard(polishBoard(movePawn(1, 0, 0, 0, polishBoard)))
#print(fp.append(1, fp.Array(2)))
#print(fp.compareProp("a", {"a": 1}, {"b": 2}))


print(game.validation.validatePlayerMove(
  game.ValidationDependencies(polishBoard, encodeKey),
  game.Move(playerOne, game.Coordinates(0, 3), game.Coordinates(1, 4))
))

#print(fp.prop("a", {"a": 1}))