package service

import entity.DrawStack
import entity.Middle
import entity.Schwimmen
import view.Refreshable

/**
 * Main class of the service layer for Schwimmen card game. The purpose of this class is likely to
 * provide a centralized point for handling interactions and updates in the Schwimmen game.
 *
 * @property gameService coordinates game logic
 * @property playerService manages players
 * @property currentGame holds the active game state.
 * @property drawStack holds active state of draw stack.
 * @property middle holds active state of table cards.
 */
class SchwimmenService {

    val gameService = GameService(this)
    val playerService = PlayerService(this)

    var currentGame: Schwimmen = Schwimmen()
    var drawStack: DrawStack = DrawStack()
    var middle: Middle = Middle()

    /** addRefreshable adds the provided [newRefreshable] to all services */
    fun addRefreshable(newRefreshable: Refreshable) {
        gameService.addRefreshable(newRefreshable)
        playerService.addRefreshable(newRefreshable)
    }

    /** addRefreshables adds each of the provided [newRefreshables] to all services */
    fun addRefreshables(vararg newRefreshables: Refreshable) {
        newRefreshables.forEach { addRefreshable(it) }
    }
}
