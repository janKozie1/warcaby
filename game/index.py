from functools import wraps

import fp
import game

class GameController:
  def __init__(self, getBoard):
    self.getBoard = getBoard

    self.deps = game.MoveDependencies(game.encodeKey, game.decodeKey, game.MoveResult)
    self.validate = game.validatePlayerMove(self.deps)
    self.processMove = game.processMove(self.deps, self.validate)
    self.playerOne = game.Player(1, game.Directions()["down"])
    self.playerTwo = game.Player(2, game.Directions()["up"])

    self.state = self.__get_initial_state()

  def __get_initial_state(self):
    return game.GameState(
      activePlayer = self.playerTwo,
      board = self.getBoard(self.playerOne, self.playerTwo),
      winner = None,
      selectedCell = None,
      needsToContinueMoveFrom = None,
      error = None
    )

  def __set_state(self, newState):
    self.state = game.GameState(**fp.merge(self.state, newState))

  def reset(self):
    self.__set_state(self.__get_initial_state())

  def __get_idle_player(self):
    return self.playerOne if self.state["activePlayer"] == self.playerTwo else self.playerTwo

  def __make_move(self, otherCell):
    state = self.state
    return fp.flow(self.validate, fp.map(self.processMove))(
      game.Move(state["activePlayer"], state["board"], state["selectedCell"]["at"], otherCell["at"], state["needsToContinueMoveFrom"])
    )

  def get_players(self):
    return game.Players(self.playerOne, self.playerTwo)

  def get_state(self):
    return self.state

  def select_cell(self, cell):
    self.__set_state({"error": None})

    if not fp.isNone(self.state["winner"]):
      return

    if fp.isNone(self.state["selectedCell"]):
      if not fp.isNone(cell["pawn"]):
        return self.__set_state({"selectedCell": cell})
      return

    if game.isSameCoord(cell["at"], self.state["selectedCell"]["at"]):
      return self.__set_state({"selectedCell": None})

    result = self.__make_move(cell)
    value = result.value

    if result.isLeft():
      return self.__set_state({"error": value})

    needsToContinueMoveFrom = value["needsToContinueMoveFrom"]
    return self.__set_state({
      "board": value["board"],
      "winner": value["winner"],
      "needsToContinueMoveFrom": needsToContinueMoveFrom,
      "selectedCell": value["board"][self.deps["keyEncoder"](needsToContinueMoveFrom)] if not fp.isNone(
        needsToContinueMoveFrom
      ) else None,
      "activePlayer": self.__get_idle_player() if fp.isNone(needsToContinueMoveFrom) else self.state["activePlayer"]
    })
