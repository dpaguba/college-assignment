package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

/**
 * Test class for Game State
 */
class GameStateTest {
    // Help variables to init a Game State
    private val currentGameState  = GameState(1,
        null,
        null,
        mutableListOf(),
        mutableListOf(),
        Board(5,arrayListOf(), 3)
    )
    private val prevGameState  = GameState(0,
        null,
        currentGameState,
        mutableListOf(),
        mutableListOf(),
        Board(5,arrayListOf(), 3)
    )

    private val nextGameState  = GameState(2,
        currentGameState,
        null,
        mutableListOf(),
        mutableListOf(),
        Board(5,arrayListOf(), 3)
    )

    /**
     * Test for getCurrentPlayerIndex
     */
    @Test
    fun getCurrentPlayerIndex() {
        assertEquals(1, currentGameState.currentPlayerIndex)
    }

    /**
     * Test for setCurrentPlayerIndex
     */
    @Test
    fun setCurrentPlayerIndex() {
        currentGameState.currentPlayerIndex = 1
        assertEquals(1, currentGameState.currentPlayerIndex)
    }

    /**
     * Test for getPrevGameState
     */
    @Test
    fun getPrevGameState() {
        assertEquals(currentGameState, nextGameState.prevGameState)
    }

    /**
     * Test for setPrevGameState
     */
    @Test
    fun setPrevGameState() {
        currentGameState.prevGameState = prevGameState
        assertEquals(prevGameState, currentGameState.prevGameState)
    }

    /**
     * Test for getNextGameState
     */
    @Test
    fun getNextGameState() {
        assertEquals(currentGameState, prevGameState.nextGameState)
    }

    /**
     * Test for setNextGameState
     */
    @Test
    fun setNextGameState() {
        currentGameState.nextGameState = nextGameState
        assertEquals(nextGameState, currentGameState.nextGameState)
    }

    /**
     * Test for getBag
     */
    @Test
    fun getBag() {
        assertEquals(arrayListOf<Tile>(), currentGameState.bag)
    }

    /**
     * Test for setBag
     */
    @Test
    fun setBag() {
        val bag = arrayListOf(Tile(TileColor.BLUE, TileColor.PURPLE), Tile(TileColor.GREEN, TileColor.GREEN))
        currentGameState.bag = bag
        assertEquals(bag, currentGameState.bag)
    }

    /**
     * Test for getPlayers
     */
    @Test
    fun getPlayers() {
        assertEquals(arrayListOf<Player>(), currentGameState.players)
    }

    /**
     * Test for setPlayer
     */
    @Test
    fun setPlayers() {
        val players = arrayListOf(Player("A", PlayerType.AI), Player("B", PlayerType.LOCAL))
        currentGameState.players = players
        assertEquals(players, currentGameState.players)
    }

    /**
     * Test for getBoard
     */
    @Test
    fun getBoard() {
        assertEquals(Board(5, arrayListOf(),3), currentGameState.board)
    }

    /**
     * Test for setBoard
     */
    @Test
    fun setBoard() {
        val board = Board(5, arrayListOf(),2)
        currentGameState.board = board
        assertEquals(board,currentGameState.board)
    }
}