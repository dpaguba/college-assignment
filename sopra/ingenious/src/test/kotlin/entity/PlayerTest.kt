package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

/**
 * This is the test class for [Player]
 * methods of the class such as isinFirstRound, getScoreboard, getRack, rackIsSwappable will be tested
 */

class PlayerTest {

    private var player1 = createPlayer()

    /**
     * Create a player instance for testing
     * @return a player with initialized value
     */

    private fun createPlayer():Player{

        return Player("player1", PlayerType.LOCAL)
    }

    /**
     * Test case for player , whether they are in first round or not
     */
    @Test
    fun isInFirstRound() {
        assertEquals(true,player1.isInFirstRound)
    }

    /**
     * testing setInFirstRound
     */
    @Test
    fun setInFirstRound() {
        player1.isInFirstRound = false
        assertEquals(false, player1.isInFirstRound)
    }

    /**
     * Test case for player's remaining round
     */
    @Test
    fun getRemainingRounds() {
        assertEquals(0, player1.remainingRounds)
    }

    /**
     * testing setRemainingRounds
     */
    @Test
    fun setRemainingRounds() {
        player1.remainingRounds = 2
        assertEquals(2,player1.remainingRounds)
    }

    /**
     * Test case for player's scoreboard
     */
    @Test
    fun getScoreBoard() {
        val scoreboard1 : MutableMap <TileColor, Int> = mutableMapOf(
            Pair(TileColor.RED, 0),
            Pair(TileColor.YELLOW, 0),
            Pair(TileColor.GREEN, 0),
            Pair(TileColor.PURPLE, 0),
            Pair(TileColor.ORANGE, 0),
            Pair(TileColor.BLUE, 0))

        assertEquals(scoreboard1,player1.scoreBoard)
    }
    /**
     * testing setScoreboard
     */

    @Test
    fun setScoreBoard() {
        val scoreboard2 : MutableMap <TileColor, Int> = mutableMapOf(
            Pair(TileColor.RED, 1),
            Pair(TileColor.YELLOW, 2),
            Pair(TileColor.GREEN, 3),
            Pair(TileColor.PURPLE, 4),
            Pair(TileColor.ORANGE, 5),
            Pair(TileColor.BLUE, 6))

        player1.scoreBoard = scoreboard2

        assertEquals(scoreboard2,player1.scoreBoard)
    }

    /**
     * Test case for player's rack
     */

    @Test
    fun getRack() {
        val tile1 = Tile(TileColor.BLUE,TileColor.GREEN)
        val tile2 = Tile(TileColor.RED,TileColor.PURPLE)
        val tile3 = Tile(TileColor.ORANGE,TileColor.YELLOW)

        val rack2 = mutableListOf(tile1,tile2,tile3)
        player1.rack = rack2

        assertEquals(rack2,player1.rack)
    }

    /**
     * testing setRack
     */

    @Test
    fun setRack() {
        val tile4 = Tile(TileColor.RED,TileColor.GREEN)
        val tile5 = Tile(TileColor.BLUE,TileColor.RED)
        val tile6 = Tile(TileColor.PURPLE,TileColor.YELLOW)

        val rack3 = mutableListOf(tile4,tile5,tile6)
        player1.rack = rack3

        assertEquals(rack3,player1.rack)
    }

    /**
     * Test case for determining if the rack is swappable
     * only possible when the lowest scoring tile colour in your scoreboard is not present anywhere in your tile rack
     */

    @Test
    fun rackIsSwappable() {

        val tile1 = Tile(TileColor.BLUE,TileColor.GREEN)
        val tile2 = Tile(TileColor.RED,TileColor.PURPLE)
        val tile3 = Tile(TileColor.ORANGE,TileColor.PURPLE)
        val tile4 = Tile(TileColor.RED,TileColor.GREEN)
        val tile5 = Tile(TileColor.BLUE,TileColor.RED)
        val tile6 = Tile(TileColor.PURPLE,TileColor.GREEN)

        val rack4 = mutableListOf(tile1,tile2,tile3,tile4,tile5,tile6)

        val scoreboard3 : MutableMap <TileColor, Int> = mutableMapOf(
            Pair(TileColor.RED, 1),
            Pair(TileColor.YELLOW, 0),
            Pair(TileColor.GREEN, 3),
            Pair(TileColor.PURPLE, 3),
            Pair(TileColor.ORANGE, 5),
            Pair(TileColor.BLUE, 2))

        player1.rack = rack4
        player1.scoreBoard = scoreboard3

        assertEquals(true,player1.rackIsSwappable())

    }

    /**
     * Another test case of swappable rack
     * this time it is the case of non-swappable
     */
    @Test
    fun rackIsNonSwappable() {

        val tile1 = Tile(TileColor.BLUE,TileColor.GREEN)
        val tile2 = Tile(TileColor.RED,TileColor.PURPLE)
        val tile3 = Tile(TileColor.ORANGE,TileColor.PURPLE)
        val tile4 = Tile(TileColor.RED,TileColor.YELLOW)
        val tile5 = Tile(TileColor.BLUE,TileColor.RED)
        val tile6 = Tile(TileColor.PURPLE,TileColor.GREEN)

        val rack5 = mutableListOf(tile1,tile2,tile3,tile4,tile5,tile6)

        val scoreboard4 : MutableMap <TileColor, Int> = mutableMapOf(
            Pair(TileColor.RED, 1),
            Pair(TileColor.YELLOW, 0),
            Pair(TileColor.GREEN, 3),
            Pair(TileColor.PURPLE, 3),
            Pair(TileColor.ORANGE, 5),
            Pair(TileColor.BLUE, 2))

        player1.rack = rack5
        player1.scoreBoard = scoreboard4

        assertEquals(false,player1.rackIsSwappable())

    }

    /**
     * Testing player's name
     */
    @Test
    fun getName() {
        assertEquals("player1",player1.name)
    }

    /**
     * testing player's type
     */

    @Test
    fun getType() {
        assertEquals(PlayerType.LOCAL,player1.type)
    }
}