package service

import entity.Player
import entity.Schwimmen
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

/**
 * Class that provides tests for [PlayerService] by simulating the usecase of every function inside
 * [PlayerService]
 */
class PlayerServiceTest {
    /** tests if the amount of player is 0 by default. */
//    @Test
//    fun createPlayer() {
//        val schwimmenService = SchwimmenService()
//        schwimmenService.currentGame = Schwimmen()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        gameService.startGame()
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        assertFalse(game.players.isNotEmpty())
//        playerService.createPlayer("Dmytro")
//        playerService.createPlayer("Max")
//        playerService.createPlayer("Anna")
//        assertEquals(3, game.players.size)
//        assertEquals("Dmytro", game.players[0].name)
//        assertEquals("Max", game.players[1].name)
//        assertEquals("Anna", game.players[2].name)
//    }

    /** tests if turn is passed to the next player */
//    @Test
//    fun pass() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        assertEquals(0, game.passCounter)
//        assertEquals("Dmytro", game.currentPlayer.name)
//        playerService.pass()
//        assertEquals(1, game.passCounter)
//        assertEquals("Max", game.currentPlayer.name)
//        playerService.pass()
//        assertEquals(2, game.passCounter)
//        assertEquals("Anna", game.currentPlayer.name)
//    }

    /** tests if game ends after it was knocked */
//    @Test
//    fun knock() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        playerService.knock()
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        assertTrue(game.players[0].hasKnocked)
//    }

    /** test if one hand card can be swapped by one table card. */
//    @Test
//    fun swapOne() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        val middle = schwimmenService.middle
//        val drawStack = schwimmenService.drawStack
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        if (middle != null && drawStack != null) {
//            val firstMiddleCard = middle.middle[0]
//            val firstHandCard = game.players[0].hand[0]
//            playerService.swapOne(firstHandCard, firstMiddleCard)
//            assertEquals(game.players[0].hand[0].toString(), firstMiddleCard.toString())
//            assertEquals(middle.middle[0].toString(), firstHandCard.toString())
//        }
//    }

    /** tests if all hand cards can be swapped by all table cards */
//    @Test
//    fun swapAll() {
//        val schwimmenService = SchwimmenService()
//        val gameService = GameService(schwimmenService)
//        val playerService = PlayerService(schwimmenService)
//        val middle = schwimmenService.middle
//        val drawStack = schwimmenService.drawStack
//        gameService.startGame()
//        gameService.schwimmenService.currentGame?.players =
//                mutableListOf(Player("Dmytro"), Player("Max"), Player("Anna"))
//        val game = gameService.schwimmenService.currentGame
//        checkNotNull(game)
//        if (middle != null && drawStack != null) {
//            val middleCards = middle.middle
//            val handCards = game.players[0].hand
//            playerService.swapAll()
//            assertEquals(game.players[0].hand[0].toString(), middleCards[0].toString())
//            assertEquals(game.players[0].hand[1].toString(), middleCards[1].toString())
//            assertEquals(game.players[0].hand[2].toString(), middleCards[2].toString())
//            assertEquals(middle.middle[0].toString(), handCards[0].toString())
//            assertEquals(middle.middle[1].toString(), handCards[1].toString())
//            assertEquals(middle.middle[2].toString(), handCards[2].toString())
//        }
//    }
}
