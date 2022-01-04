from functools import wraps

import fp
import game

class GameController:
  def __init__(self, validateMove, validatePossibleMove, processMove, dependencies, getBoard):
    self._getBoard = getBoard

    self._deps = dependencies
    self._validate = validateMove(self._deps)
    self._processMove = processMove(self._deps, validatePossibleMove(self._deps))
    self._playerOne = game.Player(1, game.Directions()["down"])
    self._playerTwo = game.Player(2, game.Directions()["up"])

    self._state = self._get_initial_state()

  def _get_initial_state(self):
    return game.GameState(
      activePlayer = self._playerTwo,
      board = self._getBoard(self._playerOne, self._playerTwo),
      winner = None,
      selectedCell = None,
      needsToContinueMoveFrom = None,
      error = None
    )

  def _set_state(self, newState):
    """state setter, merges old and partial update to create new state"""
    self._state = game.GameState(**fp.merge(self._state, newState))
    return self._state

  def reset(self):
    return self._set_state(self._get_initial_state())

  def _get_idle_player(self):
    """determines which player is not active, so that they can be switched"""
    return self._playerOne if self._state["activePlayer"] == self._playerTwo else self._playerTwo

  def _make_move(self, otherCell):
    """composes validation and board transformation to move a pawn"""

    state = self._state
    return fp.flow(self._validate, fp.map(self._processMove))(
      game.Move(state["activePlayer"], state["board"], state["selectedCell"]["at"], otherCell["at"], state["needsToContinueMoveFrom"])
    )

  def get_players(self):
    return game.Players(self._playerOne, self._playerTwo)

  def get_state(self):
    return self._state

  def select_cell(self, cell):
    """determines when to make a move, handles cell selection and deselection"""
    self._set_state({"error": None})

    if not fp.isNone(self._state["winner"]):
      return self._set_state({})

    if fp.isNone(self._state["selectedCell"]):
      if not fp.isNone(cell["pawn"]):
        return self._set_state({"selectedCell": cell})
      return self._set_state({})

    if game.isSameCoord(cell["at"], self._state["selectedCell"]["at"]):
      return self._set_state({"selectedCell": None})

    result = self._make_move(cell)
    value = result.value

    if result.isLeft():
      return self._set_state({"error": value})

    needsToContinueMoveFrom = value["needsToContinueMoveFrom"]
    return self._set_state({
      "board": value["board"],
      "winner": value["winner"],
      "needsToContinueMoveFrom": needsToContinueMoveFrom,
      "selectedCell": value["board"][self._deps["keyEncoder"](needsToContinueMoveFrom)] if not fp.isNone(
        needsToContinueMoveFrom
      ) else None,
      "activePlayer": self._get_idle_player() if fp.isNone(needsToContinueMoveFrom) else self._state["activePlayer"]
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
