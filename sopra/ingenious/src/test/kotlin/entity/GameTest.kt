package entity

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

/**
 * Test class for the [Game] entity.
 */
class GameTest {

    /**
     * Tests the [Game.hasNextGameState] method.
     */
    @Test
    fun testHasNextGameState() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        game.createNextGameState()
        assertTrue(game.hasNextGameState())
    }

    /**
     * Tests the [Game.hasPrevGameState] method.
     */
    @Test
    fun testHasPrevGameState() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        assertFalse(game.hasPrevGameState())
        game.createNextGameState()
    }

    /**
     * Tests the [Game.switchPrevGameState] method.
     */
    @Test
    fun testSwitchPrevGameState() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        assertThrows(IllegalStateException::class.java) { game.switchPrevGameState() }
        game.createNextGameState()
        game.createNextGameState()
        game.createNextGameState()
        val prevState = game.switchPrevGameState()
        assertEquals(1, game.currentGameStateIndex)
        assertEquals(prevState, game.currentGameState)
    }

    /**
     * Tests the [Game.switchNextGameState] method.
     */
    @Test
    fun testSwitchNextGameState() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        assertThrows(IllegalStateException::class.java) { game.switchNextGameState() }
        game.createNextGameState()
        game.createNextGameState()
        game.createNextGameState()
        game.switchPrevGameState()
        val nextState = game.switchNextGameState()
        assertEquals(3, game.currentGameStateIndex)
        assertEquals(nextState, game.currentGameState)
    }

    /**
     * Tests the [Game.createNextGameState] method.
     */
    @Test
    fun testCreateNextGameState() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        game.createNextGameState()
        assertEquals(2, game.gameStateList.size)
        assertNotNull(game.currentGameState)
    }

    /**
     * Tests the [Game.copyBag] method.
     */
    @Test
    fun testCopyBag() {
        val game = Game(isNetworkGame = false, isTeamMode = false)
        val copy = game.copyBag()
        assertEquals(game.currentGameState.bag, copy)
        assertNotSame(game.currentGameState.bag, copy)
    }

}

# Modified 2025-08-11 10:24:32