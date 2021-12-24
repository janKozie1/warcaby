
import fp
import game

@fp.curry
def create_board(dimensions, mapping_fn):
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
            lambda y_coord: mapping_fn(y_coord, x_coord)
          ),
          fp.value 
        ))
      ),
      fp.value
    )),
  )).join()

@fp.curry
def polishBoardPlacementRules(getPlayerOnePawn, getPlayerTwoPawn, y, x):
  if (x + y) % 2 == 1:
    if y < 4: 
      return getPlayerTwoPawn()
    if y > 5:
      return getPlayerOnePawn()
    
  return None


playerA = game.Player(1)
playerB = game.Player(2)

make10x10Board = create_board(fp.Array(10, 10))
polishBoard = make10x10Board(polishBoardPlacementRules(lambda: game.Pawn(playerA), lambda: game.Pawn(playerB)))


fp.forEach(print, polishBoard)