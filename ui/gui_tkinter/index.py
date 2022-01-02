from tkinter import *
from tkinter import ttk
from functools import wraps

import fp
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
    self.__init_frame()
    self.__init_players()
    self.__init_board(getBoard)

    self.deps = game.MoveDependencies(game.encodeKey, game.decodeKey, game.MoveResult)
    self.validate = game.validatePlayerMove(self.deps)
    self.processMove = game.processMove(self.deps)
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
    
  def __init_board(self, getBoard):
    self.board = getBoard(self.playerOne, self.playerTwo)
    self.board_repr = fp.mapDict(lambda _, key: StringVar(), self.board)

    self.selectedCell = None

  def __init_ui(self):
    self.errorVar = StringVar(value = self.error)
    self.activePlayerVar = StringVar(value = self.__player_repr(self.activePlayer))

    Label(
      self.window,
      textvariable = self.activePlayerVar
    ).grid(column = 0, row = 0, columnspan = 9)

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
    ).grid(column = 0, row = 11, columnspan=9)

  def __cell_repr(self, cell):
    def pawn(str):
      pawn = cell["pawn"]

      if fp.isNone(pawn):
        return ""

      if game.isQueen(pawn):
        return "d"
      
      return ""
        
    def color(str):
      if game.cellHasOwner(self.playerOne, cell):
        return f"C{str}"
      
      if game.cellHasOwner(self.playerTwo, cell):
        return f"B{str}"

      return ""

    def selection(str):
      if cell == self.selectedCell:
        return f"[{str}]"
      return str

    return fp.flow(pawn, color, selection)("")

  def __player_repr(self, player):
    return f'{player["id"]}'

  def __swap_active_oplayer(self):
    self.activePlayer = self.playerOne if self.activePlayer == self.playerTwo else self.playerTwo

  def makeMove(self, otherCell):
    return fp.flow(self.validate, fp.map(self.processMove))(
      game.Move(self.activePlayer, self.board, self.selectedCell["at"], otherCell["at"])
    )

  @withRerender
  def cellClickHandler(self, cell):
    self.error = None

    # moves = game.getPossibleMoves(self.deps, self.validate, self.board, self.activePlayer,cell["at"])
    # moves_with_enemy = game.getCoordinatesWithDestroyablePawns(self. deps, self.validate, self.board, self.activePlayer, cell["at"])

    # print(fp.mapDict(lambda val, key: len(val), moves))
    # print(fp.mapDict(lambda val, key: len(val), moves_with_enemy))
  
    if fp.isNone(self.selectedCell):
      if not fp.isNone(cell["pawn"]):
        self.selectedCell = cell
    elif cell == self.selectedCell:
      self.selectedCell = None
    else:
      result = self.makeMove(cell)
  
      if result.isRight():
        self.board = result.value["board"]
        self.selectedCell = None

        if (result.value["shouldSwitchPlayers"]):
          self.__swap_active_oplayer()
      else:
        self.error = result.value

  def render(self):
    fp.forEachDict(
      lambda strVar, key: strVar.set(self.__cell_repr(self.board[key])
    ), self.board_repr)

    self.errorVar.set("" if fp.isNone(self.error) else f"Ruch niedozwolony: {self.error}")
    self.activePlayerVar.set(f"Tura gracza: {self.__player_repr(self.activePlayer)}")
