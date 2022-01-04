import game
import ui
import snapshots


ui.TkinterGUI(game.createDefaultGameConroller())
#ui.TkinterGUI(game.createDefaultGameConrollerFromSnapshot(snapshots.multiple_moves_possible))