package service

import edu.udo.cs.sopra.ntf.ExampleMessage
import edu.udo.cs.sopra.ntf.IngeniousEndTurnMessage
import edu.udo.cs.sopra.ntf.IngeniousGameInitMessage
import edu.udo.cs.sopra.ntf.IngeniousPlaceMessage
import tools.aqua.bgw.core.BoardGameApplication
import tools.aqua.bgw.net.client.BoardGameClient
import tools.aqua.bgw.net.client.NetworkLogging
import tools.aqua.bgw.net.common.annotations.GameActionReceiver
import tools.aqua.bgw.net.common.notification.PlayerJoinedNotification
import tools.aqua.bgw.net.common.notification.PlayerLeftNotification
import tools.aqua.bgw.net.common.response.*
import view.Application
import kotlin.system.exitProcess

/**
 *  [BoardGameClient] implementation for network communication.
 *
 * @param networkService the [NetworkService] to potentially forward received messages to.
 */
class IngeniousNetworkClient(
    playerName: String,
    host: String,
    secret: String,
    var networkService: NetworkService
): BoardGameClient(playerName, host, secret, NetworkLogging.INFO) {

    /** the identifier of this game session; can be null if no session started yet. */
    var sessionID: String? = null

    /** safes All joining players names */
    //var otherPlayerNames = mutableListOf<String>()

    /**
     * Handle a [CreateGameResponse] sent by the server. Will await the guest player when its
     * status is [CreateGameResponseStatus.SUCCESS]. As recovery from network problems is not
     * implemented in Ingeious, the method disconnects from the server and throws an
     * [IllegalStateException] otherwise.
     *
     * @throws IllegalStateException if status != success or currently not waiting for a game creation response.
     */
    override fun onCreateGameResponse(response: CreateGameResponse) {
        BoardGameApplication.runOnGUIThread {
            check(networkService.connectionState == ConnectionState.WAIT_FOR_HOST_CONFIRMATION)
            { "unexpected CreateGameResponse" }

            when (response.status) {
                CreateGameResponseStatus.SUCCESS -> {
                    networkService.updateConnectionState(ConnectionState.WAIT_FOR_PLAYER_JOIN)
                    sessionID = response.sessionID

                }
                else -> disconnectAndError(response.status)
            }

        }
    }



    /**
     * Handle a [JoinGameResponse] sent by the server. Will await the init message when its
     * status is [JoinGameResponseStatus.SUCCESS]. As recovery from network problems is not
     * implemented in Ingeious, the method disconnects from the server and throws an
     * [IllegalStateException] otherwise.
     *
     * @throws IllegalStateException if status != success or currently not waiting for a join game response.
     */
    override fun onJoinGameResponse(response: JoinGameResponse) {
        BoardGameApplication.runOnGUIThread {
            check(networkService.connectionState == ConnectionState.WAIT_FOR_JOIN_CONFIRMATION)
            { "unexpected JoinGameResponse" }

            when (response.status) {
                JoinGameResponseStatus.SUCCESS -> {
                    sessionID = response.sessionID
                    networkService.updateConnectionState(ConnectionState.WAIT_FOR_GAME_INIT)
                }
                else -> disconnectAndError(response.status)
            }
        }
    }

    /**
     * Handle a [PlayerJoinedNotification] sent by the server. Will add a dummy network player to the game
     *
     * @throws IllegalStateException if not currently expecting any guests to join.
     */
    override fun onPlayerJoined(notification: PlayerJoinedNotification) {
        BoardGameApplication.runOnGUIThread {
            check(networkService.connectionState == ConnectionState.WAIT_FOR_PLAYER_JOIN )
            { "not awaiting any guests."}

            networkService.addNetworkPlayer(notification.sender)
        }
    }

    /**
     * Handle a [GameActionResponse] sent by the server. Does nothing when its
     * status is [GameActionResponseStatus.SUCCESS]. As recovery from network problems is not
     * implemented in Ingeious, the method disconnects from the server and throws an
     * [IllegalStateException] otherwise.
     */
    override fun onGameActionResponse(response: GameActionResponse) {
        BoardGameApplication.runOnGUIThread {
            check(networkService.connectionState == ConnectionState.PLAYING_MY_TURN ||
                    networkService.connectionState == ConnectionState.WAITING_FOR_OPPONENT_TURNS||
                    networkService.connectionState == ConnectionState.WAIT_FOR_PLAYER_JOIN||
                    networkService.connectionState == ConnectionState.WAIT_FOR_GAME_INIT)
            { "not currently playing in a network game."}

            when (response.status) {
                GameActionResponseStatus.SUCCESS -> {} // do nothing in this case
                else -> disconnectAndError(response.status)
            }
        }
    }

    /**
     * when a player leaves, close the game
     */
    override fun onPlayerLeft(notification: PlayerLeftNotification) {
        println("Player Left ${notification.sender}")
        println("Closing the game now")
        exitProcess(0)
        //networkService.updateConnectionState(ConnectionState.DISCONNECTED)

    }




    /**
     * handle a [IngeniousGameInitMessage] sent by the server
     */
    @Suppress("UNUSED_PARAMETER", "unused")
    @GameActionReceiver
    fun onInitReceived(message: IngeniousGameInitMessage, sender: String) {
        BoardGameApplication.runOnGUIThread {
            networkService.startNewJoinedGame(message)
        }
    }



    /**
     * handle a [IngeniousPlaceMessage] sent by the server
     */
    @Suppress("UNUSED_PARAMETER", "unused")
    @GameActionReceiver
    fun onIngeniousPlaceMessage(message: IngeniousPlaceMessage, sender: String){

        BoardGameApplication.runOnGUIThread {
            println("$sender send: $message")
            networkService.receiveIngeniousPlaceMessage(message)
        }
    }

    /**
     * handle a [ExampleMessage] sent by the server
     */
    @Suppress("UNUSED_PARAMETER", "unused")
    @GameActionReceiver
    fun onExampleMessage(message: ExampleMessage, sender: String){
       //implemented to fight RedMessages/Warnings
    }


    /**
     * handle a [IngeniousEndTurnMessage] sent by the server
     */
    @Suppress("UNUSED_PARAMETER", "unused")
    @GameActionReceiver
    fun onIngeniousEndTurnMessage(message: IngeniousEndTurnMessage, sender: String){
        BoardGameApplication.runOnGUIThread {
            networkService.receiveIngeniousEndTurnMessage(message)
        }
    }

    private fun disconnectAndError(message: Any ) {
        networkService.disconnect()

    }
}