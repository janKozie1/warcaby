import unittest

import game
import snapshots

class TestGameController(unittest.TestCase):
  def test_1(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.default_board)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["6-5"]
    cellP2_Move1 = lambda: state("board")["7-4"]

    cellP1_Start1 = lambda: state("board")["7-2"]
    cellP1_Move1 = lambda: state("board")["6-3"]

    cellP2_Start2 = lambda: state("board")["7-6"]
    cellP2_Move2 = lambda: state("board")["6-5"]

    cellP1_Start2 = lambda: state("board")["1-2"]
    cellP1_Move2 = lambda: state("board")["0-3"]

    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_Move1())
    self.assertEqual(cellP2_Start1()["pawn"], None)
    self.assertDictEqual(cellP2_Move1()["pawn"]["owner"], players["playerTwo"])
    self.assertDictEqual(state("activePlayer"), players["playerOne"])

    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())
    self.assertEqual(cellP1_Start1()["pawn"], None)
    self.assertDictEqual(cellP1_Move1()["pawn"]["owner"], players["playerOne"])
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    controller.select_cell(cellP2_Start2())
    controller.select_cell(cellP2_Move2())
    self.assertEqual(cellP2_Start2()["pawn"], None)
    self.assertDictEqual(cellP2_Move2()["pawn"]["owner"], players["playerTwo"])
    self.assertDictEqual(state("activePlayer"), players["playerOne"])

    controller.select_cell(cellP1_Start2())
    controller.select_cell(cellP1_Move2())
    self.assertEqual(cellP1_Start2()["pawn"], None)
    self.assertDictEqual(cellP1_Move2()["pawn"]["owner"], players["playerOne"])
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

  def test_2(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.default_board)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["0-5"]
    cellP2_InvalidMove1 = lambda: state("board")["0-4"]
    cellP2_InvalidMove2 = lambda: state("board")["1-6"]
    cellP2_InvalidMove3 = lambda: state("board")["2-3"]

    cellP1_Start1 = lambda: state("board")["1-2"]
    cellP1_Move1 = lambda: state("board")["0-3"]

    controller.select_cell(cellP2_Start1())

    controller.select_cell(cellP2_InvalidMove1())
    self.assertEqual(state("error"), "has to move pawn diagonally")
    self.assertDictEqual(cellP2_Start1()["pawn"]["owner"], players["playerTwo"])
    self.assertEqual(cellP2_InvalidMove1()["pawn"], None)
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    controller.select_cell(cellP2_InvalidMove2())
    self.assertEqual(state("error"), "has to end on an empty tile")

    controller.select_cell(cellP2_InvalidMove3())
    self.assertEqual(state("error"), "has to land after enemy's pawn or has to move by one cell")

    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())
    self.assertEqual(state("error"), "has to move pawn owned by the player")

  def test_3(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.single_jump_possible)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    board = lambda: state("board")
    prevBoard = board()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["3-4"]
    cellP2_Move1 = lambda: state("board")["5-2"]

    cellP1_Start1 = lambda: state("board")["6-1"]
    cellP1_Move1 = lambda: state("board")["4-3"]

    prevBoard = board()
    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_Move1())
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))
    self.assertDictEqual(state("activePlayer"), players["playerOne"])

    prevBoard = board()
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

  def test_4(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.double_jump_possible)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])
    self.assertEqual(state("needsToContinueMoveFrom"), None)
    self.assertEqual(state("selectedCell"), None)

    cellStart = lambda: state("board")["5-4"]
    cellJump1 = lambda: state("board")["3-2"]
    cellJump2 = lambda: state("board")["5-0"]

    cellWrong = lambda: state("board")["7-4"]
    cellWrongJump = lambda: state("board")["6-3"]

    controller.select_cell(cellStart())
    self.assertDictEqual(state("selectedCell"), cellStart())

    controller.select_cell(cellJump1())
    self.assertDictEqual(state("selectedCell"), cellJump1())
    self.assertDictEqual(state("needsToContinueMoveFrom"), cellJump1()["at"])

    controller.select_cell(cellJump1())
    controller.select_cell(cellWrong())
    controller.select_cell(cellWrongJump())
    self.assertDictEqual(state("selectedCell"), cellWrong())
    self.assertEqual(state("error"), "has to continue previous move")

    controller.select_cell(cellWrong())
    controller.select_cell(cellJump1())

    controller.select_cell(cellJump2())
    self.assertEqual(state("selectedCell"), None)
    self.assertEqual(state("needsToContinueMoveFrom"), None)

    self.assertTrue(game.hasQueen(cellJump2()))
    self.assertDictEqual(state("activePlayer"), players["playerOne"])
    self.assertEqual(state("needsToContinueMoveFrom"), None)
    self.assertEqual(state("selectedCell"), None)

  def test_5(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.multiple_moves_possible)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    board = lambda: state("board")
    prevBoard = board()

    cellP2_Start1 = lambda: state("board")["4-7"]
    cellP2_Move1 = lambda: state("board")["5-6"]

    cellP1_Start1 = lambda: state("board")["3-2"]
    cellP1_Move1 = lambda: state("board")["2-3"]

    cellP2_Start2 = lambda: state("board")["3-4"]
    cellP2_Move2 = lambda: state("board")["1-2"]

    cellP1_Start2 = lambda: state("board")["2-1"]
    cellP1_Move2 = lambda: state("board")["0-3"]
    cellP1_Move3 = lambda: state("board")["2-5"]
    cellP1_Move4 = lambda: state("board")["4-7"]

    controller.select_cell(cellP2_Start1())
    self.assertDictEqual(state("selectedCell"), cellP2_Start1())

    prevBoard = board()
    controller.select_cell(cellP2_Move1())
    self.assertEqual(state("selectedCell"), None)
    self.assertDictEqual(state("activePlayer"), players["playerOne"])
    self.assertFalse(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())
    self.assertEqual(state("selectedCell"), None)
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])
    self.assertFalse(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP2_Start2())
    controller.select_cell(cellP2_Move2())
    self.assertEqual(state("selectedCell"), None)
    self.assertDictEqual(state("activePlayer"), players["playerOne"])
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP1_Start2())
    controller.select_cell(cellP1_Move2())
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP1_Move3())
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP1_Move4())
    self.assertEqual(state("selectedCell"), None)
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])
    self.assertTrue(game.hasQueen(cellP1_Move4()))
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

  def test_6(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.with_queen)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    board = lambda: state("board")
    prevBoard = board()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["0-5"]
    cellP2_Move1 = lambda: state("board")["1-4"]

    cellP1_Start1 = lambda: state("board")["4-7"]
    cellP1_Move1 = lambda: state("board")["0-3"]

    prevBoard = board()
    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_Move1())
    self.assertFalse(game.pawnWasRemoved(board(), prevBoard))

    prevBoard = board()
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

  def test_7(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.few_moves_from_winning)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["7-6"]
    cellP2_Move1 = lambda: state("board")["6-5"]

    cellP1_Start1 = lambda: state("board")["5-4"]
    cellP1_Move1 = lambda: state("board")["7-6"]

    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_Move1())
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())

    self.assertDictEqual(state("winner")["player"], players["playerOne"])

  def test_8(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.few_moves_from_winning)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    prevState = controller.get_state()

    cellP2_Start1 = lambda: state("board")["7-6"]
    cellP2_Move1 = lambda: state("board")["6-5"]

    cellP1_Start1 = lambda: state("board")["5-4"]
    cellP1_Move1 = lambda: state("board")["7-6"]

    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_Move1())
    controller.select_cell(cellP1_Start1())
    controller.select_cell(cellP1_Move1())

    self.assertDictEqual(state("winner")["player"], players["playerOne"])

    self.assertNotEqual(prevState, controller.get_state())
    controller.reset()
    self.assertDictEqual(prevState, controller.get_state())

  def test_requiresJumpToBeMade(self):
    controller = game.createDefaultGameConrollerFromSnapshot(snapshots.single_jump_possible)
    state = lambda key: controller.get_state()[key]
    players = controller.get_players()

    board = lambda: state("board")
    prevBoard = board()

    self.assertDictEqual(state("activePlayer"), players["playerTwo"])

    cellP2_Start1 = lambda: state("board")["3-4"]
    cellP2_InvalidMove1 = lambda: state("board")["2-3"]
    cellP2_Move1 = lambda: state("board")["5-2"]

    prevBoard = board()
    controller.select_cell(cellP2_Start1())
    controller.select_cell(cellP2_InvalidMove1())
    self.assertDictEqual(state("activePlayer"), players["playerTwo"])
    self.assertEqual(state("error"), "has to jump over enemy pawn if available")
    self.assertFalse(game.pawnWasRemoved(board(), prevBoard))

    controller.select_cell(cellP2_Move1())
    self.assertDictEqual(state("activePlayer"), players["playerOne"])
    self.assertEqual(state("error"), None)
    self.assertTrue(game.pawnWasRemoved(board(), prevBoard))

if __name__ == '__main__':
    unittest.main()
