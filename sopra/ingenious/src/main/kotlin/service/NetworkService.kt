package service

import edu.udo.cs.sopra.ntf.*
import entity.*

/**
 * Service responsible for network communication in the Ingenious game.
 * @property rootService The rootService for Ingenious
 */
class NetworkService(private val rootService: RootService) : AbstractRefreshingService() {

    companion object {
        /** URL of the BGW net server hosted for SoPra participants */
        const val SERVER_ADDRESS = "sopra.cs.tu-dortmund.de:80/bgw-net/connect"

        /** Name of the game as registered with the server */
        const val GAME_ID = "Ingenious"
    }

    //private var client: IngeniousNetworkClient
    var connectionState = ConnectionState.DISCONNECTED

    /** Network Client, null for offline games     */
    var client: IngeniousNetworkClient? = null
        private set
    private val secret = "23_c_ingenious"
    private var playertype = PlayerType.LOCAL

    /**
     * Connects to server and creates a new game session.
     *
     * @param name Player name.
     * @param sessionID identifier of the hosted session (to be used by guest on join)
     * @param playerType The type of player
     * @throws IllegalStateException if already connected to another game or connection attempt fails
     */
    fun hostGame(name: String, sessionID: String?, playerType: PlayerType) {
        if (!connect(name)) {
            error("Connection failed")
        }
        updateConnectionState(ConnectionState.CONNECTED)

        if (sessionID.isNullOrBlank()) {
            client?.createGame(GAME_ID, "Welcome!")
        } else {
            client?.createGame(GAME_ID, sessionID, "Welcome!")
        }
        playertype = playerType
        rootService.game.currentGameState.players.add(Player(name, playerType))
        updateConnectionState(ConnectionState.WAIT_FOR_HOST_CONFIRMATION)
        onAllRefreshables { refreshAfterNetPlayersChanged() }
    }

    /**
     * adds a player to the playerList
     *
     * @param name name of joiningPlayer
     * @throws IllegalStateException if a 5th player wants to join
     */
    fun addNetworkPlayer(name: String) {
        if (rootService.game.currentGameState.players.size == 4) {
            throw IllegalStateException("Too many players want to join")
        }
        rootService.game.currentGameState.players.add(Player(name, PlayerType.NETWORK))
        onAllRefreshables { refreshAfterNetPlayersChanged() }
    }

    /**
     * Connects to server and joins a game session as guest player.
     *
     * @param name Player name.
     * @param sessionID identifier of the joined session (as defined by host on create)
     * @param playerType The type of player
     * @throws IllegalStateException if already connected to another game or connection attempt fails
     */
    fun joinGame(name: String, sessionID: String, playerType: PlayerType) {
        if (!connect(name)) {
            onAllRefreshables { refreshError("connection failed") }
        }
        updateConnectionState(ConnectionState.CONNECTED)

        client?.joinGame(sessionID, "Hello!")

        playertype = playerType
        rootService.game.currentGameState.players.add(Player(name, playerType))
        updateConnectionState(ConnectionState.WAIT_FOR_JOIN_CONFIRMATION)
        Thread.sleep(20)
        onAllRefreshables { refreshAfterNetPlayersChanged() }
    }

    /**
     * Connects to server, sets the [NetworkService.client] if successful and returns `true` on success.
     *
     * secret Network secret. Must not be blank (i.e. empty or only whitespaces)
     * @param name Player name. Must not be blank
     *
     * @throws IllegalArgumentException if secret or name is blank
     * @throws IllegalStateException if already connected to another game
     */
    private fun connect(name: String): Boolean {
        require(connectionState == ConnectionState.DISCONNECTED && client == null)
        { "already connected to another game" }

        require(name.isNotBlank()) { "player name must be given" }

        val newClient =
            IngeniousNetworkClient(
                playerName = name,
                host = SERVER_ADDRESS,
                secret = secret,
                networkService = this
            )
        try {
            return if (newClient.connect()) {
                this.client = newClient
                true
            } else {
                false
            }
        } catch (e: IllegalStateException) {
            println(e.message)
        }
        return false
    }

    /**
     * Disconnects the [client] from the server, nulls it and updates the
     * [connectionState] to [ConnectionState.DISCONNECTED]. Can safely be called
     * even if no connection is currently active.
     */
    fun disconnect() {
        client?.apply {
            if (sessionID != null) leaveGame("Goodbye!")
            if (isOpen) disconnect()
        }
        client = null
        if (connectionState != ConnectionState.DISCONNECTED) {
            updateConnectionState(ConnectionState.DISCONNECTED)
        }
        //rootService.gameService.endGame()
    }

    /**
     *   This function starts the online game as a Host
     *
     *   with a CONNECTION == WAIT_FOR_GAME_INIT
     *   @param isTeamGame indicator for gameMode
     *   @throws IllegalStateException if there are too many or not enough players
     */
    fun startNewHostedGame(isTeamGame: Boolean) {

        val gameState = rootService.game.currentGameState
        if (gameState.players.size < 2) {
            onAllRefreshables { refreshError("not enough players") }
            return
        } else if (gameState.players.size > 4) {
            onAllRefreshables { refreshError("too many players") }
            return
        }
        if (isTeamGame) {
            if (gameState.players.size != 4) {
                onAllRefreshables { refreshError("The player amount does not match the GameType") }
                return
            }
        }

        //set the game up
        rootService.game.isNetworkGame = true
        rootService.game.isTeamMode = isTeamGame

        val bag = rootService.gameService.bagInit()
        //send stuff
        sendIngeniousGameInitMessage(isTeamGame, bag)

        //fill players
        for (player in gameState.players) {
            repeat(6) {
                player.rack.add(bag.removeLast())
            }
        }
        gameState.board = Board(radius = gameState.players.size + 3, playerSize = gameState.players.size)
        gameState.bag = bag
        //set the current player up
        gameState.currentPlayerIndex = 0
        gameState.players[0].remainingRounds++

        rootService.game.createNextGameState()
        onAllRefreshables { refreshAfterLoadGame() }

        if (gameState.players[0].type != PlayerType.NETWORK) {
            updateConnectionState(ConnectionState.PLAYING_MY_TURN)
        } else {
            updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        }
    }


    /**
     * This function starts the online game as a client, when a Game Init message is recieved
     * assumes the local player will be setup before
     * @param message The game init message
     */
    fun startNewJoinedGame(message: IngeniousGameInitMessage) {
        val playerNames = message.playerList
        val playerList = mutableListOf<Player>()
        val bag: MutableList<Tile> = message.firstStack.map {
            Tile(messageToColor(it.firstColor), (messageToColor(it.secondColor)))
        }.toMutableList()
        rootService.game.isNetworkGame = true
        rootService.game.isTeamMode = message.isTeamMode


        // make a list of players
        for (name in playerNames) {
            val player: Player = if (client?.playerName == name) {
                Player(name, playertype)
            } else {
                Player(name, PlayerType.NETWORK)
            }
            //fill their Racks
            repeat(6) {
                player.rack.add(bag.removeLast())
            }
            playerList.add(player)
        }

        // now override all everything in gamestate
        val gameState = rootService.game.currentGameState
        gameState.players = playerList
        gameState.bag = bag
        gameState.board = Board(radius = playerList.size + 3, playerSize = playerList.size)

        gameState.currentPlayerIndex = 0
        gameState.players[0].remainingRounds++

        if (gameState.players[0].type != PlayerType.NETWORK) {
            updateConnectionState(ConnectionState.PLAYING_MY_TURN)
        } else {
            updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        }
        rootService.game.createNextGameState()
        onAllRefreshables { refreshAfterLoadGame() }
    }


    /**
     * this method makes sends a GameInitMessage
     *
     * @param teamGame if this game is FFA or a 2v2 game mode
     * @param bag the tileList, that will be sent to the others
     */
    private fun sendIngeniousGameInitMessage(teamGame: Boolean, bag: MutableList<Tile>) {
        val gameState = rootService.game.currentGameState
        //create array of players
        val playerList = gameState.players.map { it.name }

        val stack = bag.map {
            IngeniousTileMessage(colorToMessage(it.firstColor), colorToMessage(it.secondColor))
        }
        val message = IngeniousGameInitMessage(
            playerList,
            teamGame,
            stack
        )
        client?.sendGameActionMessage(message)
    }

    /**
     * converts a local TileColor to the agreed upon IngeniousColorMessage
     *
     * @return IngeniousColorMessage
     * @throws IllegalStateException if the given tileColor is outOfBounds or Empty
     */
    private fun colorToMessage(tileColor: TileColor): IngeniousColorMessage {
        return when (tileColor) {
            TileColor.RED -> IngeniousColorMessage.RED
            TileColor.GREEN -> IngeniousColorMessage.GREEN
            TileColor.BLUE -> IngeniousColorMessage.BLUE
            TileColor.YELLOW -> IngeniousColorMessage.YELLOW
            TileColor.ORANGE -> IngeniousColorMessage.ORANGE
            TileColor.PURPLE -> IngeniousColorMessage.PURPLE
            else -> throw IllegalArgumentException("Tile color is illegal")
        }
    }

    /**
     * converts the agreed upon IngeniousColorMessage into a local Tilecolor
     *
     * @return TileColor
     */
    private fun messageToColor(messageColor: IngeniousColorMessage): TileColor {
        return when (messageColor) {
            IngeniousColorMessage.RED -> TileColor.RED
            IngeniousColorMessage.BLUE -> TileColor.BLUE
            IngeniousColorMessage.GREEN -> TileColor.GREEN
            IngeniousColorMessage.YELLOW -> TileColor.YELLOW
            IngeniousColorMessage.ORANGE -> TileColor.ORANGE
            IngeniousColorMessage.PURPLE -> TileColor.PURPLE
        }
    }


    /**
     * Send to the other Players, that your Turn has ended
     *
     * all handling will be local
     * with a CONNECTION == PLAYING MY TURN
     *
     * @param swapAllFlag indicates, that the player selected to swap their hand
     * @param gameEnded indicates, that the game has ended, bei either having a full board or the currentplayer reached
     * max points
     * @param firstBag a shuffled version of the draw pile
     */
    fun sendIngeniousEndTurnMessage(swapAllFlag: Boolean, gameEnded: Boolean, firstBag: MutableList<Tile>) {
        updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        val message = IngeniousEndTurnMessage(
            swapAllFlag,
            gameEnded,
            firstBag.map { IngeniousTileMessage(colorToMessage(it.firstColor), colorToMessage(it.secondColor)) }
        )
        updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        client?.sendGameActionMessage(message)


    }


    /**
     * This method makes an endTurn functionality for all recieved endTurnMessages
     *
     * @param message a recieved IngeniousEndTurnMessage
     */
    fun receiveIngeniousEndTurnMessage(message: IngeniousEndTurnMessage) {
        println(rootService.game.currentGameState.currentPlayerIndex)
        if (message.gameEnded) {
            updateConnectionState(ConnectionState.DISCONNECTED)
            rootService.gameService.endGame()
        } else if (message.swapAllFlag) {
            //copied from playerService swapAll
            val gameState = rootService.game.currentGameState
            val currentPlayer = gameState.players[gameState.currentPlayerIndex]
            val bag = gameState.bag
            //val removedTiles = mutableListOf<Tile>()

            if (currentPlayer.rackIsSwappable()) {
                //fill player rack with 6 new tiles
                currentPlayer.rack.removeIf { true }
                repeat(6) {
                    currentPlayer.rack.add(bag.removeLast())
                }
                //replace bag with the newly send one
                gameState.bag = message.newPile.map {
                    Tile(messageToColor(it.firstColor), messageToColor(it.secondColor))
                }
                    .toMutableList()
            } else {
                throw IllegalArgumentException("Rack is not swappable!")
            }
            // set up the next round
            rootService.gameService.setUpNextRound()
        } else {

            val gameState = rootService.game.currentGameState
            val currentPlayer = gameState.players[gameState.currentPlayerIndex]
            if(currentPlayer.type == PlayerType.NETWORK){
                if(currentPlayer.rackIsSwappable()){
                    rootService.playerService.fillRack()
                }
            }


        }
        /*

        if (rootService.game.currentGameState.players[rootService.game.currentGameState.currentPlayerIndex].type ==
        PlayerType.LOCAL){
            updateConnectionState(ConnectionState.PLAYING_MY_TURN)
        }
        else{
            updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        }

         */

    }

    /**
     * Sends a [IngeniousPlaceMessage] to other players in Network games
     *
     * It has no logic. It only converts from local variables to network variables
     *
     * @param firstColor first tileColor of the Tile
     * @param secondColor second tileColor of the Tile
     * @param firstX the horizontal coordinate of the first part of the tile
     * @param firstY the vertical coordinate of the first part of the tile
     * @param secondX the horizontal coordinate of the first part of the tile
     * @param secondY the vertical coordinate of the first part of the tile
     */
    fun sendIngeniousPlaceMessage(
        firstColor: TileColor,
        secondColor: TileColor,
        firstX: Int,
        firstY: Int,
        secondX: Int,
        secondY: Int
    ) {
        //just send
        val message = IngeniousPlaceMessage(
            colorToMessage(firstColor),
            colorToMessage(secondColor),
            firstX, firstY,
            secondX, secondY
        )
        client?.sendGameActionMessage(message)
    }

    /**
     * Converts parameters given in the message to parameters needed by [PlayerService.placeTile]
     *
     * @param message a given [IngeniousPlaceMessage]
     */
    fun receiveIngeniousPlaceMessage(message: IngeniousPlaceMessage) {
        val mTile = Tile(messageToColor(message.firstColor), messageToColor(message.secondColor))
        val gameState = rootService.game.currentGameState
        val currentPlayer = gameState.players[gameState.currentPlayerIndex]
        var tilePos = 0

        for ((pos, pTile) in currentPlayer.rack.withIndex()) {
            //find the index of the given mTile
            if ((mTile.firstColor == pTile.firstColor && mTile.secondColor == pTile.secondColor) ||
                (mTile.firstColor == pTile.secondColor && mTile.secondColor == pTile.firstColor)
            ) {
                tilePos = pos
                break
            }
        }

        val orientation: TileOrientation = when (Pair(
            message.secondXPosition - message.firstXPosition,
            message.secondYPosition - message.firstYPosition
        )) {
            Pair(0, 1) -> TileOrientation.RIGHT
            Pair(1, 0) -> TileOrientation.DOWN_RIGHT
            Pair(1, -1) -> TileOrientation.DOWN_LEFT
            Pair(0, -1) -> TileOrientation.LEFT
            Pair(-1, 0) -> TileOrientation.UP_LEFT
            Pair(-1, 1) -> TileOrientation.UP_RIGHT
            else -> throw IllegalArgumentException("the given coordinates are not next to each other")
        }
        println("PlaceNet: ${message.firstXPosition},${message.firstYPosition}")
        rootService.playerService.placeTile(tilePos, message.firstXPosition, message.firstYPosition, orientation)

    }

    /**
     * Updates the [connectionState] to [newState] and notifies
     * all refreshables via Refreshable.refreshConnectionState
     */
    fun updateConnectionState(newState: ConnectionState) {
        this.connectionState = newState
        onAllRefreshables {
            refreshConnectionState(newState)
        }
    }
}