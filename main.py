
import fp
import game

@fp.curry
def createBoard(dimensions, mapping_fn):
  return fp.head(dimensions).chain(
    lambda x_size: fp.second(dimensions).map(fp.flow(
      fp.fill(x_size), 
      fp.map(fp.fillWithIndex)
    )
  )).map(fp.flow(
    fp.withIndex,
    fp.map(fp.flow(
      lambda row_with_index: fp.second(row_with_index).map(
        lambda row: row.map(fp.flow(
          lambda x_coord: fp.head(row_with_index).map(
            lambda y_coord: mapping_fn(x_coord, y_coord)
          ),
          fp.value 
        ))
      ),
      fp.value
    )),
  )).join()

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
def placeInCell(coords, thing, board):
  return fp.map(fp.map(fp.ifElse(lambda cell: game.Cell(coordsy, thing), fp.identity, game.isCellAt(coords))))(board)

@fp.curry
def takePawn(coords, board):
  return fp.flow(
    fp.join,
    fp.find(game.isCellAt(coords)),
    fp.chain(fp.prop("pawn"))
  )(board)

removePawn = lambda coords, board: placeInCell(coords, None, board)
placePawn = placeInCell

def movePawn(coordsFrom, coordsTo, board):
  pawnToMove = takePawn(coordsFrom, board)
  return placePawn(coordsTo, pawnToMove, removePawn(coordsFrom, board))


playerOne = game.Player(1)
playerTwo = game.Player(2)

make10x10Board = createBoard(fp.Array(10, 10))
polishBoard = make10x10Board(polishBoardPlacementRules(playerOne, playerTwo))

def cellRepr(cell):
  if cell["pawn"] is None:
    return "-"

  return  f'{cell["pawn"]["owner"]["id"]}'

def printBoard(board):
  fp.forEach(lambda row: print(row.map(cellRepr)), board)



#printBoard(polishBoard(movePawn(1, 0, 0, 0, polishBoard)))

print(fp.compareProp("a", {"a": 1}, {"b": 2}))

#print(fp.prop("a", {"a": 1}))