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
    self._gameController = gameController

    self._init_frame()
    self._init_ui()

    self.render()
    self._window.mainloop()

  def _init_frame(self):
    self._window = Tk()
    self._window.title("Warcaby")

    self._mainframe = ttk.Frame(self._window)
    self._mainframe.grid(column = 0, row = 0, sticky=(N, W, E, S))

  def _init_ui(self):
    state = self._gameController.get_state()

    self._errorVar = StringVar(value = state["error"])
    self._playerVar = StringVar(value = self._player_repr(state["activePlayer"]))

    boardWidth = game.getBoardWidth(state["board"])
    boardHeight = game.getBoardHeight(state["board"])

    self._board_repr = fp.mapDict(lambda _, __: StringVar(), state["board"])

    Label(
      self._window,
      textvariable = self._playerVar
    ).grid(column = 0, row = 0, columnspan = boardWidth)

    fp.forEachDict(lambda cell, key: Button(
      self._window,
      textvariable = self._board_repr[key],
      height = 5,
      width = 10,
      command = lambda c = key: self.cellClickHandler(self._gameController.get_state()["board"][c])
    ).grid(column = cell["at"]["x"], row = cell["at"]["y"] + 1), state["board"])

    Label(
      self._window,
      textvariable = self._errorVar
    ).grid(column = 0, row = boardHeight + 2, columnspan = boardWidth)

    #padding
    Label(
      self._window,
      text = ""
    ).grid(column = 0, row = boardHeight + 3, columnspan = boardWidth)

    Button(
      self._window,
      text="Reset",
      command = self.resetButtonClickHandler,
    ).grid(column = 0, row = boardHeight + 4, columnspan = boardWidth)

  def _cell_repr(self, cell):
    selectedCell = self._gameController.get_state()["selectedCell"]

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

      return f"{self._player_repr(pawn['owner'])}{str}"

    def selection(str):
      if fp.isNone(selectedCell):
        return str

      if game.isSameCoord(cell["at"], selectedCell["at"]):
        return f"[{str}]"
      return str

    return fp.flow(pawn, color, selection)("")

  def _player_repr(self, player):
    players = self._gameController.get_players()

    if compareProp("id", player, players["playerOne"]):
      return "C"

    if compareProp("id", player, players["playerTwo"]):
      return "B"

    return None

  def _get_winner_text(self, winner):
    if fp.isNone(winner):
      return None

    if fp.isNone(winner["player"]):
      return "Game end: Draw"
    else:
      return f"Game end: player {self._player_repr(winner['player'])} won"

  @withRerender
  def resetButtonClickHandler(self):
    self._gameController.reset()

  @withRerender
  def cellClickHandler(self, cell):
    prevState = self._gameController.get_state()
    state = self._gameController.select_cell(cell)

    if fp.isNone(prevState["winner"]) and not fp.isNone(state["winner"]):
      messagebox.showinfo(title = "Game end", message = self._get_winner_text(state["winner"]))

    if not fp.isNone(state["error"]):
      messagebox.showerror(title = "Invalid move", message = state["error"])


  def render(self):
    state = self._gameController.get_state()

    fp.forEachDict(
      lambda strVar, key: strVar.set(self._cell_repr(state['board'][key])
    ), self._board_repr)

    self._errorVar.set("" if fp.isNone(state["error"]) else f"Invalid move: {state['error']}")

    if fp.isNone(state["winner"]):
      self._playerVar.set(f"Player's turn: {self._player_repr(state['activePlayer'])}")
    else:
      self._playerVar.set(self._get_winner_text(state['winner']))
