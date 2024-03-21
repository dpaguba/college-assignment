package service

import entity.PlayerType
import entity.Tile
import entity.TileColor
import entity.TileOrientation
import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*
import kotlin.test.assertFails

/**
 * This is the test for the player service
 */
class PlayerServiceTest {
    private val rootService = RootService()
    private val gameService = rootService.gameService
    private val playerService = rootService.playerService

    private fun init4PlayerGame() {
        gameService.addPlayer("Player 1", PlayerType.LOCAL)
        gameService.addPlayer("Player 2", PlayerType.LOCAL)
        gameService.addPlayer("Player 3", PlayerType.LOCAL)
        gameService.addPlayer("Player 4", PlayerType.LOCAL)

        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }

    /**
     * Compares two racks by comparing the tiles mem location.
     *
     * @return true if both racks are the same
     * @return false if they are not
     */
    private fun compareRack(rack1: MutableList<Tile>, rack2: MutableList<Tile>): Boolean {
        if (rack1.size != rack2.size)
            return false
        for ((i, itemR1) in rack1.withIndex()) {
            if (itemR1 !== rack2[i])
                return false
            if (itemR1 !== rack2[i])
                return false
        }
        return true
    }

    /**
     * Tests place tile
     */
    @Test
    fun placeTile() {
        // create a test refreshable
        val dummyRefreshable = TestRefreshable()
        rootService.addRefreshable(dummyRefreshable)
        dummyRefreshable.reset()
        // inti a new game
        init4PlayerGame()
        // testing if a wrong placed first tile gets caught
        // storing rack and player index
        var rackBefore = rootService.game.currentGameState.players[0].rack.toMutableList()
        var playerIndexBefore = rootService.game.currentGameState.currentPlayerIndex
        assertFails(block = {
            playerService.placeTile(0, -2, 3, TileOrientation.UP_LEFT)
        })
        // testing if the rack was not modified
        assertTrue(
            compareRack(rackBefore, rootService.game.currentGameState.players[0].rack),
            "Oops. The Rack shouldn't have changed"
        )
        assertEquals(playerIndexBefore, rootService.game.currentGameState.currentPlayerIndex)
        // no refresh should have been called
        assertFalse(dummyRefreshable.refreshAfterTurnCalled)

        // testing if a wrong placed tile (on a start color) gets caught
        // storing rack and player index
        rackBefore = rootService.game.currentGameState.players[0].rack.toMutableList()
        playerIndexBefore = rootService.game.currentGameState.currentPlayerIndex
        assertFails(block = {
            playerService.placeTile(0, -5, 0, TileOrientation.UP_LEFT)
        })
        // testing if the rack was not modified
        assertTrue(
            compareRack(rackBefore, rootService.game.currentGameState.players[0].rack),
            "Oops. The Rack shouldn't have changed"
        )
        assertEquals(playerIndexBefore, rootService.game.currentGameState.currentPlayerIndex)
        // no refresh should have been called
        assertFalse(dummyRefreshable.refreshAfterTurnCalled)

        // now doing a valid place:
        // storing rack
        rackBefore = rootService.game.currentGameState.players[0].rack.toMutableList()
        playerIndexBefore = rootService.game.currentGameState.currentPlayerIndex
        // placing the tile
        playerService.placeTile(0, -5, 1, TileOrientation.UP_LEFT)
        // checking rack and player index
        assertFalse(
            (compareRack(rackBefore, rootService.game.currentGameState.players[0].rack)),
            "Oops. The Rack should have changed"
        )
        assertEquals(playerIndexBefore + 1, rootService.game.currentGameState.currentPlayerIndex)
        // refresh should have been called
        assertTrue(dummyRefreshable.refreshAfterTurnCalled)
        dummyRefreshable.reset()

        // let's put another tile on the same start point. It should fail.
        // storing rack
        rackBefore = rootService.game.currentGameState.players[0].rack.toMutableList()
        playerIndexBefore = rootService.game.currentGameState.currentPlayerIndex
        // placing the tile
        assertFails(block = {
            playerService.placeTile(0, -5, -1, TileOrientation.UP_RIGHT)
        })
        // checking rack and player index
        assertTrue(
            (compareRack(rackBefore, rootService.game.currentGameState.players[0].rack)),
            "Oops. The Rack shouldn't have changed"
        )
        assertEquals(playerIndexBefore, rootService.game.currentGameState.currentPlayerIndex)
        // no refresh should have been called
        assertFalse(dummyRefreshable.refreshAfterTurnCalled)

        // now lets place three more valid tiles
        playerService.placeTile(1, -3, 4, TileOrientation.UP_LEFT)
        playerService.placeTile(2, 1, -4, TileOrientation.UP_LEFT)
        playerService.placeTile(3, 5, 1, TileOrientation.UP_LEFT)
        dummyRefreshable.reset()

        // now we should be able to place a tile anywhere
        // storing rack
        rackBefore = rootService.game.currentGameState.players[0].rack.toMutableList()
        playerIndexBefore = rootService.game.currentGameState.currentPlayerIndex
        // placing the tile
        playerService.placeTile(0, -3, 2, TileOrientation.UP_LEFT)
        // checking rack and player index
        assertFalse(
            (compareRack(rackBefore, rootService.game.currentGameState.players[0].rack)),
            "Oops. The Rack should have changed"
        )
        assertEquals(playerIndexBefore + 1, rootService.game.currentGameState.currentPlayerIndex)
        // refresh should have been called
        assertTrue(dummyRefreshable.refreshAfterTurnCalled)
        dummyRefreshable.reset()

        // TTesting the scoreboard
        testUpdateScoreboard()
    }

    /**
     * This must be called with an initiated game!!!
     */
    private fun testUpdateScoreboard() {
        //get a dummy refreshable
        val dummyRefreshable = TestRefreshable()
        rootService.addRefreshable(dummyRefreshable)
        rootService.game.currentGameState
        // clear the scoreboards
        for (player in rootService.game.currentGameState.players) {
            for (color in TileColor.values().dropLast(2))
                player.scoreBoard[color] = 0
        }
        // now we clear the center of the board to play around in there
        for (column in -4..4) {
            for (row in -4..4) {
                val x = rootService.game.currentGameState.board.indexToRealIndex(column,row).first
                val y = rootService.game.currentGameState.board.indexToRealIndex(column,row).second
                rootService.game.currentGameState.board.fields[x][y] = TileColor.EMPTY
            }
        }
        // getting the index of the testPlayer (just the one whose turn it is currently)
        val tP = rootService.game.currentGameState.currentPlayerIndex
        val tPsRack = rootService.game.currentGameState.players[tP].rack
        // let's manipulate the rack to our likings
        tPsRack[0] = Tile(TileColor.BLUE, TileColor.BLUE)
        tPsRack[1] = Tile(TileColor.BLUE, TileColor.BLUE)
        tPsRack[2] = Tile(TileColor.GREEN, TileColor.GREEN)
        tPsRack[3] = Tile(TileColor.ORANGE, TileColor.ORANGE)
        tPsRack[4] = Tile(TileColor.BLUE, TileColor.BLUE)
        tPsRack[5] = Tile(TileColor.BLUE, TileColor.BLUE)

        // place the tiles
        playerService.placeTile(0,0,0,TileOrientation.RIGHT)
        var tPsScoreBoard = rootService.game.currentGameState.players[tP].scoreBoard
        // reset the player index
        rootService.game.currentGameState.currentPlayerIndex = tP
        // the scoreboard should still be at 0
        assertEquals(0, tPsScoreBoard[TileColor.BLUE])
        // place another tile:
        playerService.placeTile(0,0,2,TileOrientation.RIGHT)
        tPsScoreBoard = rootService.game.currentGameState.players[tP].scoreBoard
        // the scoreboard should be at 2
        assertEquals(2, tPsScoreBoard[TileColor.BLUE])
    }

    /**
     * Tests setColorOnField
     */
    @Test
    fun setColorOnField() {
        // init game
        init4PlayerGame()
        val currentGame = rootService.game.currentGameState
        // now we can set the colors
        for (column in -7..7) {
            val range = currentGame.board.getColumnRange(column)
            for (row in range.first..range.second) {
                val expectedColor = TileColor.values().dropLast(2).random()
                // set the color
                playerService.setColorOnField(column, row, expectedColor)
                val x = currentGame.board.indexToRealIndex(column,row).first
                val y = currentGame.board.indexToRealIndex(column,row).second
                // both colors should be the same
                assertEquals(expectedColor.ordinal, currentGame.board.fields[x][y].ordinal)
            }
        }
        //test if setting a color out of bounds fails
        assertFails { playerService.setColorOnField(10,-10,TileColor.ORANGE) }
    }
}