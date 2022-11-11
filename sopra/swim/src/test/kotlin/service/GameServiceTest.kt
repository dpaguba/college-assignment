package service

import entity.Player
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

/**
 * Class that provides tests for [GameService] by simulating the usecase of every function inside
 * [GameService]
 */
class GameServiceTest {

    /** Tests if a new game is created correctly */
//    @Test
//    fun startGame() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        val middle = schwimmenService.middle
//        val drawStack = schwimmenService.drawStack
//        gameService.startGame()
//        playerService.createPlayer("Dmytro")
//        assertNull(gameService.schwimmenService.currentGame)
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        assertEquals(3, game.players.size)
//        assertEquals("Dmytro", game.players[0].name)
//        assertEquals("Max", game.players[1].name)
//        assertEquals("Anna", game.players[2].name)
//        assertEquals("Dmytro", game.currentPlayer.name)
//        for (player in game.players) {
//            assertEquals(3, player.hand.size)
//        }
//        if (middle != null && drawStack != null) {
//            assertEquals(3, middle.middle.size)
//            assertEquals(20, drawStack.drawStack.size)
//        }
//    }
    /** Tests if checkPassCounter function works */
//    @Test
//    fun checkPassCounter() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        gameService.checkPassCounter()
//        assertEquals(0, game.passCounter)
//        game.passCounter = 3
//        assertEquals(3, game.passCounter)
//        gameService.checkPassCounter()
//        assertEquals(0, game.passCounter)
//        game.passCounter = 1
//        assertEquals(1, game.passCounter)
//    }

    /**
     * Checks if old table cards are not the same with new. Checks if cards deck size has changed
     */
//    @Test
//    fun renewMiddle() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val middle = schwimmenService.middle
//        val drawStack = schwimmenService.drawStack
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        val oldMiddle = middle?.middle
//        val oldDrawStackSize = drawStack?.drawStack?.size
//        gameService.renewMiddle()
//        assertNotEquals(middle?.middle.toString(), oldMiddle.toString())
//        if (oldDrawStackSize != null) {
//            assertEquals(oldDrawStackSize - 3, drawStack.drawStack.size)
//        }
//    }
//
//    /** Tests if turn is changed */
//    @Test
//    fun finishTurn() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        assertEquals("Dmytro", game.currentPlayer.name)
//        gameService.finishTurn()
//        assertEquals("Max", game.currentPlayer.name)
//        gameService.finishTurn()
//        assertEquals("Anna", game.currentPlayer.name)
//        gameService.finishTurn()
//        assertEquals("Dmytro", game.currentPlayer.name)
//    }
}

# Modified 2025-08-11 10:24:34