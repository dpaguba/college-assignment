package service

import entity.Game
import entity.PlayerType
import entity.TileColor
import org.junit.jupiter.api.Assertions.assertThrows
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

/**
 * This is the test for the IOService
 */
class IOServiceTest {
    private var rootService = RootService()
    private val iOService = rootService.ioService
    private val gameService = rootService.gameService
    private val playerService = rootService.playerService

    /**
     * Inits 4 players
     */
    private fun init4Players() {
        for (i in 1..4) {
            gameService.addPlayer("Player $i", PlayerType.LOCAL)
        }
    }

    /**
     * Inits a game with 4 players
     */
    private fun init4Game() {
        init4Players()
        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }

    /**
     * Tests getSavedGames
     */
    @Test
    fun getSavedGames() {
        println(iOService.getSavedGames())
    }

    /**
     * Tests storeGame
     */
    @Test
    fun storeGame() {
        init4Game()

        assertThrows(IllegalArgumentException::class.java) {
            iOService.storeGame(4)
        }

        val board = rootService.game.currentGameState.board
        var column = board.getRowRange(0).first

        while (column <= board.getRowRange(0).second) {
            val colRange = board.getColumnRange(column)
            for (row in colRange.first..colRange.second) {
                playerService.setColorOnField(column, row, TileColor.GREEN)
            }
            column++
        }

        println(rootService.game.currentGameState.board.fields.toString())
        println(rootService.game.currentGameState.board.fields.size)

        iOService.storeGame(1)

        iOService.loadGame(1)
        println(rootService.game.currentGameState.board.fields.toString())
        //println(rootService.game.gameStateList[rootService.game.currentGameStateIndex - 1])
    }

    /*
    @Test
    fun loadGame() {
        init4Game()
        iOService.loadGame(1)
        println(rootService.game.currentGameState.board.fields.toString())
        println(rootService.game.gameStateList[rootService.game.currentGameStateIndex - 1])
    }*/

    /**
     * Tests everything together
     */
    @Test
    fun fullTest() {
        init4Game()
        assertThrows(IllegalArgumentException::class.java) {
            iOService.storeGame(4)
        }

        val board = rootService.game.currentGameState.board
        var column = board.getRowRange(0).first

        while (column <= board.getRowRange(0).second) {
            val colRange = board.getColumnRange(column)
            for (row in colRange.first..colRange.second) {
                playerService.setColorOnField(column, row, TileColor.GREEN)
            }
            column++
        }
        val input = rootService.game.currentGameState.board.fields.toString()

        println("Stored: ${rootService.game.currentGameState.board.fields}")
        iOService.storeGame(1)
        rootService.game = Game(isNetworkGame = true, isTeamMode = true)
        iOService.loadGame(1)
        val output = rootService.game.currentGameState.board.fields.toString()
        println("Loaded: ${rootService.game.currentGameState.board.fields}")
        assertTrue(input == output)
    }
}