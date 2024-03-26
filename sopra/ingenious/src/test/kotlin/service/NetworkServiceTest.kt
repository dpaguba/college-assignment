package service

import entity.*
import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*
import kotlin.random.Random

/**
 * This is the test for the network service
 */
class NetworkServiceTest {
    private val rootService = RootService()
    private val network = rootService.networkService
    private val gameService = rootService.gameService

    /**
     * helper function
     */
    private fun init2Players(){
        for (i in 1 .. 2){
            gameService.addPlayer("Player $i", PlayerType.LOCAL)
        }
    }

    /**
     * test if the Server is reachable
     */
    @Test
    fun hostGame() {
        network.hostGame("Player1","TestOne",PlayerType.LOCAL)
        assert(network.connectionState == ConnectionState.WAIT_FOR_HOST_CONFIRMATION ||
                network.connectionState == ConnectionState.WAIT_FOR_PLAYER_JOIN||
                network.connectionState == ConnectionState.CONNECTED)
        init2Players()
        network.disconnect()
        assertEquals(ConnectionState.DISCONNECTED,network.connectionState)
    }

    /**
     * test a local helper function
     */
    @Test
    fun addNetworkPlayer() {
        network.addNetworkPlayer("Tom")
        assertEquals(1,rootService.game.currentGameState.players.size)
    }


    /**
     * This is The Main Test for NetworkServe/client
     * this simulates a game
     */
    @Test
    fun hostGameAndJoinGame() {
        val rootGuest = RootService()

        network.hostGame("Gruppe1 player1", "Gruppe01: Test Verbindung${Random.nextInt()}",PlayerType.LOCAL)
        rootService.waitForState(ConnectionState.WAIT_FOR_PLAYER_JOIN)
        val sessionID = network.client?.sessionID
        assertNotNull (sessionID)
        rootGuest.networkService.joinGame("Gruppe1 player2",sessionID!!,PlayerType.LOCAL)
        //Thread.sleep(5000)
        rootGuest.waitForState(ConnectionState.WAIT_FOR_GAME_INIT)
        rootService.networkService.startNewHostedGame(false)

        println("sleep 5sec, to wait for guest joining")
        Thread.sleep(5000)

        assertEquals(rootService.game.currentGameState.players[0].rack[0],
            rootGuest.game.currentGameState.players[0].rack[0])

        rootService.playerService.placeTile(0,4,0,TileOrientation.UP_LEFT)
        println("sleep 5sec, to wait for guest receiving a place tile at 4,0")
        Thread.sleep(5000)


        //set all players to not be in first turn
        rootService.game.currentGameState.players.forEach { it.isInFirstRound = false }
        rootGuest.game.currentGameState.players.forEach { it.isInFirstRound = false }
        rootGuest.playerService.placeTile(0,0,0,TileOrientation.DOWN_RIGHT)

        println("sleep 5sec, to wait for root for receiving a place tile at 0,0")
        Thread.sleep(5000)
        //check, if both players have the same tiles
        //rootService.waitForState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        assertEquals(rootGuest.game.currentGameState.board.getTileColor(0,0),
            rootService.game.currentGameState.board.getTileColor(0,0))
        assertEquals(rootGuest.game.currentGameState.players[1].rack[5],
            rootService.game.currentGameState.players[1].rack[5])

        //set the current player to be swappable
        val currentRoot = rootService.game.currentGameState.players[0]
        currentRoot.rack = arrayListOf()
        repeat(6){
           currentRoot.rack.add(Tile(TileColor.BLUE,TileColor.BLUE))
        }
        currentRoot.scoreBoard[TileColor.RED] = 1
        currentRoot.scoreBoard[TileColor.YELLOW] = 18
        currentRoot.scoreBoard[TileColor.GREEN] = 18
        currentRoot.scoreBoard[TileColor.ORANGE] = 18
        currentRoot.scoreBoard[TileColor.PURPLE] = 18
        currentRoot.scoreBoard[TileColor.BLUE] = 18
        //sync the guest client
        val currentguest = rootGuest.game.currentGameState.players[0]
        currentguest.rack = arrayListOf()
        repeat(6){
            currentguest.rack.add(Tile(TileColor.BLUE,TileColor.BLUE))
        }
        currentguest.scoreBoard[TileColor.RED] = 1
        currentguest.scoreBoard[TileColor.YELLOW] = 18
        currentguest.scoreBoard[TileColor.GREEN] = 18
        currentguest.scoreBoard[TileColor.ORANGE] = 18
        currentguest.scoreBoard[TileColor.PURPLE] = 18
        currentguest.scoreBoard[TileColor.BLUE] = 18

        rootService.playerService.placeTile(0,2,2,TileOrientation.RIGHT)
        rootService.playerService.swapRack()
        Thread.sleep(5000)
        assertEquals(rootService.game.currentGameState.bag,rootGuest.game.currentGameState.bag)

        //force the 2player to win
        rootService.game.currentGameState.players[0].scoreBoard[TileColor.RED] = 18
        //rootGuest.game.currentGameState.players[0].scoreBoard[TileColor.RED] = 18
        rootGuest.playerService.placeTile(0,-2,-2,TileOrientation.DOWN_RIGHT)
        println("sleep 5sec, to wait for guest to place")
        Thread.sleep(5000)
        rootService.playerService.placeTile(0,-2,2,TileOrientation.RIGHT)
        println("sleep 5sec, to wait for host to win")
        Thread.sleep(5000)
        //either test with a test refreshable, if both have called a refresh or if both disconnect
        assertEquals(ConnectionState.DISCONNECTED,rootService.networkService.connectionState)
        assertEquals(ConnectionState.DISCONNECTED,rootGuest.networkService.connectionState)
    }


    /**
     * busy waiting for the game represented by this [RootService] to reach the desired network [state].
     * Polls the desired state every 100 ms until the [timeout] is reached.
     *
     * This is a simplification hack for testing purposes, so that tests can be linearized on
     * a single thread.
     *
     * @param state the desired network state to reach
     * @param timeout maximum milliseconds to wait (default: 5000)
     *
     * @throws IllegalStateException if desired state is not reached within the [timeout]
     */
    private fun RootService.waitForState(state: ConnectionState, timeout: Int = 5000) {
        var timePassed = 0
        while (timePassed < timeout) {
            if (networkService.connectionState == state)
                return
            else {
                Thread.sleep(100)
                timePassed += 100
            }
        }
        error("Did not arrive at state $state after waiting $timeout ms")
    }
}