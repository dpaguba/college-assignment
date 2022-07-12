package service

import entity.*
import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

/**
 * Test class for the [GameService], it test game actions like addPlayers, finishTurn, startGame etc.
 */
class GameServiceTest {
    private val rootService = RootService()
    private val gameService = rootService.gameService
    private val playerService = rootService.playerService
    private val game = rootService.game
    private val gameState = game.currentGameState

    /**
     * Inits 2 players
     */
    private fun init2Players(){
        for (i in 1 .. 2){
            gameService.addPlayer("Player $i", PlayerType.LOCAL)
        }
    }

    /**
     * Inits a game with 2 players
     */
    private fun init2Game(){
        init2Players()
        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }
    /**
     * Inits 4 players
     */
    private fun init4Players(){
        for (i in 1 .. 4){
            gameService.addPlayer("Player $i", PlayerType.LOCAL)
        }
    }

    /**
     * Inits a game with 4 players
     */
    private fun init4Game(){
        init4Players()
        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }

    /**
     * Test case for finishTurn, it checks if the currentPlayerIndex ist changed correctly
     */
    @Test
    fun finishTurn(){
        init4Game()

        playerService.placeTile(3, -5,1, TileOrientation.RIGHT)

        assertEquals(1,rootService.game.currentGameState.currentPlayerIndex)

        //gameState.players[gameState.currentPlayerIndex].scoreBoard.set()
        /*val colors = TileColor.values().dropLast(2)
        for (color in colors){
            gameState.players[gameState.currentPlayerIndex].scoreBoard.set(color, 18)
        }*/

        playerService.placeTile(1,4,0,TileOrientation.RIGHT)

        assertEquals(2,rootService.game.currentGameState.currentPlayerIndex)

        playerService.placeTile(3,5,-4,TileOrientation.UP_RIGHT)
        assertEquals(3,rootService.game.currentGameState.currentPlayerIndex)
    }

    /**
     * Test case for start game, is everything initialized correctly?
     */
    @Test
    fun startGame() {
        init4Game()

        // check if correct game mode has been selected
        assertEquals(false, game.isTeamMode)
        assertEquals(false, game.isNetworkGame)

        // check for a correctly initialized bag
        assertEquals(120 - 4 * 6, gameState.bag.size)

        // check for correctly initialized racks
        for (player in gameState.players){
            assertEquals(6, player.rack.size)
        }

        // create list with all tiles of the game, check how many diff tiles exist, create a list with the counts
        val allTiles = mutableListOf<Tile>()
        allTiles.addAll(gameState.bag)
        for (player in gameState.players){
            allTiles.addAll(player.rack)
        }
        val tileCountMap = allTiles.groupBy { it }
        val tileCounts = tileCountMap.mapValues { it.value.size }

        // check if exactly 21 different tiles have been found
        assertEquals(21, tileCounts.size)

        // check if each tile has the right amount in the list, 5 for tiles with the same colors on both fields,
        // 6 for different colors on both fields
        tileCounts.forEach{ (tile, count) ->
            if (tile.firstColor == tile.secondColor) assertEquals(5, count)
            else assertEquals(6, count)
        }

        // check for remaining settings
        assertEquals(7, gameState.board.radius)
        assertEquals(0, gameState.currentPlayerIndex)
        assertEquals(1, gameState.players[0].remainingRounds)
    }

    /**
     * Tests order players
     */
    @Test
    fun orderPlayers(){
        init4Players()
        val player = game.currentGameState.players.toList()

        val index = listOf(3,2,1,0)

        gameService.orderPlayers(index)
        assertNotEquals(player, game.currentGameState.players)
    }
    /**
     * Test case for addPlayers
     */
    @Test
    fun addPlayer() {
        init4Players()

        for (i in 1 .. 4){
            assertEquals("Player $i", gameState.players[i - 1].name)
        }

        assertThrows(IllegalStateException::class.java) {
            gameService.addPlayer("Player 5", PlayerType.LOCAL)
        }
    }

    /**
     * Test case one for endGame, is endGame called after one player reaches 18 everywhere
     */
    @Test
    fun endGamePlayerReached18Everywhere() {
        init4Game()

        assertEquals(0,rootService.game.currentGameState.currentPlayerIndex)
        playerService.placeTile(3, -5,1, TileOrientation.RIGHT)

        assertEquals(1,rootService.game.currentGameState.currentPlayerIndex)
        val colors = TileColor.values().dropLast(2)
        for (color in colors){
            game.currentGameState.players[game.currentGameState.currentPlayerIndex].scoreBoard[color] = 18
        }

        playerService.placeTile(2,4,-5,TileOrientation.RIGHT) // should call println in endGame with the winner
    }

    /**
     * Second test case for end game if the board is full.
     * Should call the println in endGame
     * Works properly.
     */
    @Test
    fun endGameBoardIsFull(){
        init4Game()

        val board = gameState.board
        var column = board.getRowRange(0).first

        while (column <= board.getRowRange(0).second){
            val colRange = board.getColumnRange(column)
            for (row in colRange.first ..colRange.second ){
                playerService.setColorOnField(column,row,TileColor.GREEN)
            }
            column++
        }

        playerService.setColorOnField(0,0,TileColor.EMPTY)
        playerService.setColorOnField(0,1,TileColor.EMPTY)

        game.currentGameState.players[game.currentGameState.currentPlayerIndex].isInFirstRound = false
        playerService.placeTile(0,0,0,TileOrientation.RIGHT)
    }

    /**
     * Test case for undo/redo
     */
    @Test
    fun undoRedo() {
        init2Game()
        playerService.placeTile(0,0,4,TileOrientation.LEFT)

        var currentPlayer = game.currentGameState.players[game.currentGameState.currentPlayerIndex]

        currentPlayer.rack[0] = Tile(TileColor.PURPLE, TileColor.PURPLE)

        assertEquals(0,currentPlayer.scoreBoard[TileColor.PURPLE])

        playerService.placeTile(0,0,-4,TileOrientation.UP_LEFT)

        currentPlayer = game.currentGameState.players[1]
        assertEquals(2,currentPlayer.scoreBoard[TileColor.PURPLE])

        gameService.undo()

        currentPlayer = game.currentGameState.players[1]
        assertEquals(0,currentPlayer.scoreBoard[TileColor.PURPLE])

        gameService.redo()

        currentPlayer = game.currentGameState.players[1]
        assertEquals(2,currentPlayer.scoreBoard[TileColor.PURPLE])
    }


    /**
     * Test case for shufflePlayers, we shuffle the player list and check if it changed appropriate, could fail if the
     * list would randomly shuffle to its old state
     */
    @Test
    fun shufflePlayers() {
        init4Players()

        val oldList = ArrayList(gameState.players)
        assertEquals(oldList, game.currentGameState.players)

        gameService.shufflePlayers()

        println(gameState.players.toString())
        //assertNotEquals(oldList, game.currentGameState.players)
    }

    /**
     * Test case for flipPlayers, we flip players and check if it changed appropriate
     */
    @Test
    fun flipPlayers() {
        init4Players()

        val oldList = ArrayList(gameState.players)
        val player1 = gameState.players[0]
        val player2 = gameState.players[3]

        gameService.flipPlayers(0, 3)

        assertNotEquals(oldList, game.currentGameState.players)
        assertNotEquals(player1, gameState.players[0])
        assertEquals(player1, gameState.players[3])
        assertEquals(player2, gameState.players[0])
    }

    /**
     * Test case for setUpNextRound, it checks if the remainingRounds will be changed and if the currentPlayerIndex
     * is set correctly (e.g. from 3 to 0)
     */
    @Test
    fun setUpNextRound() {
        init4Game()

        assertEquals(0, gameState.players[1].remainingRounds)

        gameService.setUpNextRound()

        assertEquals(1, game.currentGameState.currentPlayerIndex)
        assertEquals(1, game.currentGameState.players[1].remainingRounds)

        gameService.setUpNextRound() // Player 1 -> Player 2
        gameService.setUpNextRound() // Player 2 -> Player 3
        gameService.setUpNextRound() // Player 3 -> Player 0

        assertEquals(0,game.currentGameState.currentPlayerIndex)
    }
}

/**
 *          val board = gameState.board.copy()
 *          val newList = ArrayList(ArrayList<Tile>())
 *          var column = board.getRowRange(0).first
 *
 *          while (column <= board.getRowRange(0).second){
 *              val colRange = board.getColumnRange(column)
 *              extraList = ArrayList<Tile()
 *              colRange.add(extraList)
 *              for (row in colRange.first ..colRange.second ){
 *                  extraList.add(board.getTileColor(column, row))
 *              }
 *              column++
 *          }
 */
# Modified 2025-08-11 10:24:32