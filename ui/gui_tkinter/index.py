from tkinter import *
from tkinter import ttk, messagebox
from functools import wraps

import fp
from fp.utils.object import compareProp
import game

def withRerender(method):
  @wraps(method)
  def wrapper(self, *args):
    result = method(self, *args)
    self.render()

    return result

  return wrapper

class TkinterGUI:
  def __init__(self, gameController):
    self.gameController = gameController

    self.__init_frame()
    self.__init_ui()

    self.render()
    self.window.mainloop()

  def __init_frame(self):
    self.window = Tk()
    self.window.title("Warcaby")

    self.mainframe = ttk.Frame(self.window)
    self.mainframe.grid(column = 0, row = 0, sticky=(N, W, E, S))

  def __init_ui(self):
    state = self.gameController.get_state()

    self.errorVar = StringVar(value = state["error"])
    self.playerVar = StringVar(value = self.__player_repr(state["activePlayer"]))

    boardWidth = game.getBoardWidth(state["board"])
    boardHeight = game.getBoardHeight(state["board"])

    self.board_repr = fp.mapDict(lambda _, __: StringVar(), state["board"])

    Label(
      self.window,
      textvariable = self.playerVar
    ).grid(column = 0, row = 0, columnspan = boardWidth)

    fp.forEachDict(lambda cell, key: Button(
      self.window,
      textvariable = self.board_repr[key],
      height = 5,
      width = 10,
      command = lambda c = key: self.cellClickHandler(self.gameController.get_state()["board"][c])
    ).grid(column = cell["at"]["x"], row = cell["at"]["y"] + 1), state["board"])

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
    selectedCell = self.gameController.get_state()["selectedCell"]

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
      if fp.isNone(selectedCell):
        return str

      if game.isSameCoord(cell["at"], selectedCell["at"]):
        return f"[{str}]"
      return str

    return fp.flow(pawn, color, selection)("")

  def __player_repr(self, player):
    players = self.gameController.get_players()

    if compareProp("id", player, players["playerOne"]):
      return "C"

    if compareProp("id", player, players["playerTwo"]):
      return "B"

    return None

  def __get_winner_text(self, winner):
    if fp.isNone(winner):
      return None

    if fp.isNone(winner["player"]):
      return "Game end: Draw"
    else:
      return f"Game end: player {self.__player_repr(winner['player'])} won"

  @withRerender
  def resetButtonClickHandler(self):
    self.gameController.reset()

  @withRerender
  def cellClickHandler(self, cell):
    self.gameController.select_cell(cell)

  def render(self):
    state = self.gameController.get_state()

    fp.forEachDict(
      lambda strVar, key: strVar.set(self.__cell_repr(state['board'][key])
    ), self.board_repr)

    self.errorVar.set("" if fp.isNone(state["error"]) else f"Invalid move: {state['error']}")

    if fp.isNone(state["winner"]):
      self.playerVar.set(f"Player's turn: {self.__player_repr(state['activePlayer'])}")
    else:
      self.playerVar.set(self.__get_winner_text(state['winner']))

    # print(state["board"])
    # print("---------------------------------")