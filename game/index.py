from functools import wraps

import fp
import game

class GameController:
  def __init__(self, validateMove, validatePossibleMove, processMove, dependencies, getBoard):
    self.__getBoard = getBoard

    self.__deps = dependencies
    self.__validate = validateMove(self.__deps)
    self.__processMove = processMove(self.__deps, validatePossibleMove(self.__deps))
    self.__playerOne = game.Player(1, game.Directions()["down"])
    self.__playerTwo = game.Player(2, game.Directions()["up"])

    self.__state = self.__get_initial_state()

  def __get_initial_state(self):
    return game.GameState(
      activePlayer = self.__playerTwo,
      board = self.__getBoard(self.__playerOne, self.__playerTwo),
      winner = None,
      selectedCell = None,
      needsToContinueMoveFrom = None,
      error = None
    )

  def __set_state(self, newState):
    self.__state = game.GameState(**fp.merge(self.__state, newState))

  def reset(self):
    self.__set_state(self.__get_initial_state())

  def __get_idle_player(self):
    return self.__playerOne if self.__state["activePlayer"] == self.__playerTwo else self.__playerTwo

  def __make_move(self, otherCell):
    state = self.__state
    return fp.flow(self.__validate, fp.map(self.__processMove))(
      game.Move(state["activePlayer"], state["board"], state["selectedCell"]["at"], otherCell["at"], state["needsToContinueMoveFrom"])
    )

  def get_players(self):
    return game.Players(self.__playerOne, self.__playerTwo)

  def get_state(self):
    return self.__state

  def select_cell(self, cell):
    self.__set_state({"error": None})

    if not fp.isNone(self.__state["winner"]):
      return

    if fp.isNone(self.__state["selectedCell"]):
      if not fp.isNone(cell["pawn"]):
        return self.__set_state({"selectedCell": cell})
      return

    if game.isSameCoord(cell["at"], self.__state["selectedCell"]["at"]):
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
      "selectedCell": value["board"][self.__deps["keyEncoder"](needsToContinueMoveFrom)] if not fp.isNone(
        needsToContinueMoveFrom
      ) else None,
      "activePlayer": self.__get_idle_player() if fp.isNone(needsToContinueMoveFrom) else self.__state["activePlayer"]
    })


createDefaultGameConroller = lambda: game.GameController(
  game.validatePlayerMove,
  game.validatePossiblePlayerMove,
  game.processMove,
  game.MoveDependencies(game.encodeKey, game.decodeKey, game.MoveResult),
  lambda playerOne, playerTwo: game.make8x8Board(
    game.englishBoardPlacementRules(playerOne, playerTwo)
  ))

createDefaultGameConrollerFromSnapshot = lambda snapshot: game.GameController(
  game.validatePlayerMove,
  game.validatePossiblePlayerMove,
  game.processMove,
  game.MoveDependencies(game.encodeKey, game.decodeKey, game.MoveResult),
  fp.wrap(snapshot)
)