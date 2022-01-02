from tkinter import *
from tkinter import ttk, messagebox
from functools import wraps

import fp
from fp.utils.object import compareProp
import game

from ui.abstract import UI

def withRerender(method):
  @wraps(method)
  def wrapper(self, *args):
    result = method(self, *args)
    self.render()

    return result

  return wrapper

class TkinterGUI(UI):
  def __init__(self, getBoard):
    self.getBoard = getBoard

    self.__init_frame()
    self.__init_players()
    self.__init_board()

    self.deps = game.MoveDependencies(game.encodeKey, game.decodeKey, game.MoveResult)
    self.validate = game.validatePlayerMove(self.deps)
    self.processMove = game.processMove(self.deps, self.validate)
    self.error = None

    self.__init_ui()
    self.render()
    self.window.mainloop()

  def __init_frame(self):
    self.window = Tk()
    self.window.title("Warcaby")

    self.mainframe = ttk.Frame(self.window)
    self.mainframe.grid(column = 0, row = 0, sticky=(N, W, E, S))

  def __init_players(self):
    self.playerOne = game.Player(1, game.Directions()["down"])
    self.playerTwo = game.Player(2, game.Directions()["up"])

    self.activePlayer = self.playerTwo
    self.winner = None

  def __init_board(self):
    self.board = self.getBoard(self.playerOne, self.playerTwo)
    self.board_repr = fp.mapDict(lambda _, __: StringVar(), self.board)

    self.selectedCell = None
    self.needsToContinueMoveFrom = None

  def __init_ui(self):
    self.errorVar = StringVar(value = self.error)
    self.playerVar = StringVar(value = self.__player_repr(self.activePlayer))

    boardWidth = game.getBoardWidth(self.board)
    boardHeight = game.getBoardHeight(self.board)

    Label(
      self.window,
      textvariable = self.playerVar
    ).grid(column = 0, row = 0, columnspan = boardWidth)

    fp.forEachDict(lambda cell, key: Button(
      self.window,
      textvariable = self.board_repr[key],
      height = 5,
      width = 10,
      command = lambda c = key: self.cellClickHandler(self.board[c])
    ).grid(column = cell["at"]["x"], row = cell["at"]["y"] + 1), self.board)

    Label(
      self.window,
      textvariable = self.errorVar
    ).grid(column = 0, row = boardHeight + 2, columnspan = boardWidth)

    #padding
    Label(
      self.window,
      text = ""
    ).grid(column = 0, row = boardHeight + 3, columnspan = boardWidth)

    Button(
      self.window,
      text="Reset",
      command = self.resetButtonClickHandler,
    ).grid(column = 0, row = boardHeight + 4, columnspan = boardWidth)

  def __cell_repr(self, cell):
    def pawn(str):
      pawn = cell["pawn"]

      if fp.isNone(pawn):
        return ""

      if game.isQueen(pawn):
        return "d"

      return ""

    def color(str):
      pawn = cell["pawn"]

      if fp.isNone(pawn):
        return str

      return f"{self.__player_repr(pawn['owner'])}{str}"

    def selection(str):
      if cell == self.selectedCell:
        return f"[{str}]"
      return str

    return fp.flow(pawn, color, selection)("")

  def __player_repr(self, player):
    if compareProp("id", player, self.playerOne):
      return "C"

    if compareProp("id", player, self.playerTwo):
      return "B"

    return None

  def __swap_active_oplayer(self):
    self.activePlayer = self.playerOne if self.activePlayer == self.playerTwo else self.playerTwo

  def __get_winner_text(self):
    if fp.isNone(self.winner):
      return None

    if fp.isNone(self.winner["player"]):
      return "Game end: Draw"
    else:
      return f"Game end: player {self.__player_repr(self.winner['player'])} won"

  def __snapshot(self):
    print(self.board)

  def makeMove(self, otherCell):
    return fp.flow(self.validate, fp.map(self.processMove))(
      game.Move(self.activePlayer, self.board, self.selectedCell["at"], otherCell["at"], self.needsToContinueMoveFrom)
    )

  @withRerender
  def resetButtonClickHandler(self):
    self.activePlayer = self.playerTwo
    self.winner = None

    self.board = self.getBoard(self.playerOne, self.playerTwo)

    self.selectedCell = None
    self.needsToContinueMoveFrom = None
    self.error = None

  @withRerender
  def cellClickHandler(self, cell):
    self.error = None

    if not fp.isNone(self.winner):
      return

    if fp.isNone(self.selectedCell):
      if not fp.isNone(cell["pawn"]):
        self.selectedCell = cell
    elif cell == self.selectedCell:
      self.selectedCell = None
    else:
      result = self.makeMove(cell)

      if result.isRight():
        self.board = result.value["board"]
        self.winner = result.value["winner"]
        self.selectedCell = None
        self.needsToContinueMoveFrom = result.value["needsToContinueMoveFrom"]

        if not fp.isNone(self.winner):
          messagebox.showinfo(title = "Game end", message = self.__get_winner_text())

        if not fp.isNone(self.needsToContinueMoveFrom):
          self.selectedCell = self.board[self.deps["keyEncoder"](self.needsToContinueMoveFrom)]
        else:
          self.__swap_active_oplayer()
      else:
        self.error = result.value

  def render(self):
    fp.forEachDict(
      lambda strVar, key: strVar.set(self.__cell_repr(self.board[key])
    ), self.board_repr)

    self.errorVar.set("" if fp.isNone(self.error) else f"Invalid move: {self.error}")

    if fp.isNone(self.winner):
      self.playerVar.set(f"Player's turn: {self.__player_repr(self.activePlayer)}")
    else:
      self.playerVar.set(self.__get_winner_text())