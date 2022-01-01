import game
import ui

# def cellRepr(cell):
#   if cell["pawn"] is None:
#     return "-"

#   return  f'{cell["pawn"]["owner"]["id"]}'

# def printBoard(board):
#   fp.flow(
#     fp.keys,
#     fp.groupBy(fp.flow(decodeKey, fp.second, fp.value)),
#     fp.values,
#     fp.map(fp.map(lambda key: fp.value(fp.prop(key, board)))),
#     fp.forEach(lambda row: print(row.map(cellRepr)))
#   )(board)


# fp.flow(
#   validate,
#   fp.map(fp.flow(process, printBoard))
# )(mv)

ui.TkinterGUI(lambda playerOne, playerTwo: game.make8x8Board(
  game.englishBoardPlacementRules(playerOne, playerTwo)
))