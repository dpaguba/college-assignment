package service

import entity.*
import tools.aqua.bgw.core.BoardGameApplication

/**
 * The Game Service, it controls the game itself, it ensures that all rules are followed
 * @property rootService The root Service of Ingenious
 */
class GameService(private val rootService: RootService) : AbstractRefreshingService() {
    /**
     * method contains gamelogic, that happens at the end of each turn(includes bonusRounds)
     *
     * Fist tests if the game can end because the board is full or a player has won.
     * Then checks if the current player has remaining bonus rounds, calls the gui and returns
     * Creates a new gameState for drawing etc.
     * Then if the player is able to swap calls the gui and returns
     *
     * the 2 draw methods have to call onAllRefreshables { refreshAfterTurn() } and set the next player
     */
    fun finishTurn() {
        //Nicolas
        //easy access to some objects
        val game = rootService.game
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]
        //decrement roundCounter
        player.remainingRounds--

        //tests for condition when the game ends
        if (gameCanEnd()) {
            endGame()
            return
        }

        //game will continue
        if (player.remainingRounds > 0) {
            println("Bonus round:")
            if (player.type != PlayerType.NETWORK) {
                onAllRefreshables { refreshAfterBonusRound() }
            }
            return
        }
        //this is a blank safeState, the playerRacks are at 6 tiles and the boards (safe)
        game.currentGameState = game.createNextGameState()
        //player can swap his rack
        print("currentplayer " + gameState.currentPlayerIndex)
        println(player.rackIsSwappable())
        if (player.rackIsSwappable()) {
            println("Is swappable")
            if (player.type != PlayerType.NETWORK) {
                onAllRefreshables { refreshAfterRackSwappable() }
            }
            return
        }

        //nothing special happens
        rootService.playerService.fillRack()
    }


    /**
     * This function checks all conditions for ending a game
     *
     * @returns if the game can end
     */
    private fun gameCanEnd(): Boolean {

        val gameState = rootService.game.currentGameState
        val game = rootService.game
        val player = gameState.players[gameState.currentPlayerIndex]
        var canEnd = true

        if (game.isTeamMode) {
            player.scoreBoard.forEach { canEnd = it.value >= 36 && canEnd }
        } else {
            player.scoreBoard.forEach { canEnd = it.value >= 18 && canEnd }
        }
        canEnd = canEnd || gameState.board.isFull()
        println("GameCanEnd: $canEnd")

        return canEnd
    }

    /**
     * Initializes the game.
     *
     * Sets the parameters of game
     * updates the bag and player rack in gameState
     */
    fun startGame(isTeamGame: Boolean, isNetworkGame: Boolean) {
        //set the game parameters


        val game = rootService.game
        game.isTeamMode = isTeamGame
        game.isNetworkGame = isNetworkGame
        //update the gameState to a viable gameState
        val gameState = game.currentGameState
        // check, if there are enough players
        if(gameState.players.size < 2){
            onAllRefreshables { refreshError("not enough players") }
            return
        }
        else if(gameState.players.size > 4){
            onAllRefreshables { refreshError("too many players") }
            return
        }
        if(isTeamGame){
            if(gameState.players.size!=4) {
                onAllRefreshables { refreshError("The player amount does not match the GameType") }
                return
            }
        }

        //give the payers tiles
        //fill the bag
        //set radius maybe even override board
        gameState.bag = bagInit()
        //fill player racks
        for (player in gameState.players) {
            repeat(6) {
                player.rack.add(gameState.bag.removeLast())
            }
        }
        gameState.board = Board(radius = gameState.players.size + 3, playerSize = gameState.players.size)

        //set the current player up
        gameState.currentPlayerIndex = 0
        gameState.players[0].remainingRounds++

        //set up the next Gamestate, where the place method will work on (playable)

        onAllRefreshables { refreshAfterLoadGame() }
        startAI()
    }

    /**
     * Starts the AI
     */
    fun startAI() {
        val currentPlayer =
            rootService.game.currentGameState.players[rootService.game.currentGameState.currentPlayerIndex]
        if (currentPlayer.type == PlayerType.AI) {
            rootService.aiService.makeMove()
        } else if (currentPlayer.type == PlayerType.AI_RANDOM) {
            rootService.aiRandomService.makeMove()
        }
    }

    /**
     * a helper method for initialising a bag
     *
     * @return a mutable list of Tiles
     */
    fun bagInit(): MutableList<Tile> {
        val bag = mutableListOf<Tile>()
        //all important colors
        val colorSet = TileColor.values().dropLast(2)
        //print(colorSet)
        //println( "colorset : ${colorSet.size}")
        for ((i, colorFst) in colorSet.withIndex()) {
            //go from pos i to last
            for (j in i..colorSet.size) {

                if (j == 6) {
                    continue
                }
                //println(j)
                val colorSnd = colorSet[j]
                if (colorFst != colorSnd) {
                    repeat(6) {
                        bag.add(Tile(colorFst, colorSnd))
                    }
                } else {
                    //same colors
                    repeat(5) {
                        bag.add(Tile(colorFst, colorSnd))
                    }
                }
            }
        }
        bag.shuffle()
        return bag
    }

    /**
     * Adds a Player to the game.
     * This Player is a dummy and has no Tiles.
     * Automatically starts when there are 4 players in the playerlist.
     *
     * @throws IllegalStateException if there are more than 4 players
     */
    fun addPlayer(name: String, playerType: PlayerType) {

        val gameState = rootService.game.currentGameState
        if (gameState.players.size == 4) {
            throw IllegalStateException("the player field is too big")
        }
        gameState.players.add(Player(name, playerType))
    }

    /**
     * ends the game(calls refreshAfterGameEnd) and calculates the names of the winner
     *
     * in TeamMode the winner will be calculated as "Player1.name and player2.name"
     */
    fun endGame() {
        val winnerPos: Int = endGameHelper()
        val gameState = rootService.game.currentGameState
        if (gameState.players.size < 1) {
            return
        }
        val winner = if (rootService.game.isTeamMode) {
            "${gameState.players[winnerPos]} and ${gameState.players[(winnerPos + 2) % 4]}"
        } else {
            gameState.players[winnerPos].name
        }

        println("Winner: $winner")

        if (rootService.game.isNetworkGame && rootService.networkService.connectionState !=
            ConnectionState.DISCONNECTED) {
            rootService.networkService.sendIngeniousEndTurnMessage(
                swapAllFlag = false,
                gameEnded = true,
                firstBag = gameState.bag
            )
            rootService.game.isNetworkGame = false
            rootService.networkService.disconnect()
        }
        onAllRefreshables { refreshAfterGameEnd(winner) }
    }

    /**
     * This is a helper method, to calculate, which player has won.
     *
     * minValLoop is the min value for each player. It gets compared to each min val
     */
    private fun endGameHelper(): Int {
        var pos = 0
        var minVal = 0
        val gameState = rootService.game.currentGameState
        for ((index, player) in gameState.players.withIndex()) {
            val minValLoop = player.scoreBoard.minOf { it.value }
            if (minValLoop > minVal) {
                pos = index
                minVal = minValLoop
            }
        }
        return pos
    }

    /**
     * Implements undo functionality, by setting the currentGame pointer to its previous (play) gameState
     *
     * It checks, if the currentGameState has 2 previous gameStates (this is the next playState). If it does, it will
     * change to said playState. If it has only one this would be the First playState, therefore it cant change back.
     *
     *
     */
    fun undo() {
        //Nicolas
        val game = rootService.game
        if (game.hasPrevGameState()) {
            game.switchPrevGameState()
        } else {
            println("no switch")
        }
        revertToSafe()
        onAllRefreshables { refreshAfterLoadGame() }
    }

    /**
     * implements redo functionality,by setting the currentGame pointer to its next gameState
     */
    fun redo() {
        val game = rootService.game
        if (game.hasNextGameState()) {
            game.switchNextGameState()
        }
        revertToSafe()
        onAllRefreshables { refreshAfterLoadGame() }

    }

    /**
     * Changes the currentGameState to its Previous version (safeState)
     *
     * revertToSafe overrides attributes that might change while playing to a state,
     * where no actions have been made by the player
     */
    private fun revertToSafe() {
        //current gameState is playState, safeState is its previous state
        val game = rootService.game
        val playState = game.currentGameState
        //ln(game.currentGameStateIndex-1>=0)
        if (game.currentGameStateIndex - 1 >= 0) {
            val safeState = game.gameStateList[game.currentGameStateIndex - 1]
            //override playState bag players and board with safeState attributes copys
            playState.bag = copyBag(safeState.bag)
            playState.players = copyPlayers(safeState.players)
            playState.board = copyBoard(safeState.board)
            // println("done")
        }
    }

    /**
     * Copys the bag and returns it
     * @param bag The bag that will be copied
     * @return A list of all tiles, that the bag contains
     */
    private fun copyBag(bag: MutableList<Tile>): MutableList<Tile> {
        //maybe it is enough to just call bag.copy(), but this is safe

        val newBag = mutableListOf<Tile>()
        for (tile in bag) {
            newBag.add(tile.copy())
        }
        return newBag

    }

    /**
     * This returns a copy of a given playerList not shallow
     *
     * copied from [Game] and changed slightly
     */
    private fun copyPlayers(players: MutableList<Player>): MutableList<Player> {

        val newPlayerList = mutableListOf<Player>()
        //create new player objects
        for (oldPlayer in players) {
            val newPlayer = Player(oldPlayer.name, oldPlayer.type)
            newPlayer.isInFirstRound = oldPlayer.isInFirstRound
            newPlayer.remainingRounds = oldPlayer.remainingRounds
            //copy all tiles from rack .copy() might be a bit overkill
            for (tile in oldPlayer.rack) {
                newPlayer.rack.add(Tile(tile.firstColor, tile.secondColor))
            }

            for (pair in oldPlayer.scoreBoard) {
                newPlayer.scoreBoard[pair.key] = pair.value
            }
            newPlayerList.add(newPlayer)
        }

        //sync the scoreBoards in teamGame
        if (rootService.game.isTeamMode) {
            newPlayerList[2].scoreBoard = newPlayerList[0].scoreBoard
            newPlayerList[3].scoreBoard = newPlayerList[1].scoreBoard
        }
        return newPlayerList

    }

    /**
     * This returns a copy of a given board not shallow
     *
     * copied from [Game] and changed slightly
     */
    private fun copyBoard(board: Board): Board {
        val newBoard = board.copy()
        //copy the fields arraylist to a new one
        val newField = arrayListOf<ArrayList<TileColor>>()
        for (list in board.fields) {
            val nList = arrayListOf<TileColor>()
            for ((i, color) in list.withIndex()) {
                nList.add(i, color)
            }
            newField.add(nList)
        }
        //override the fields-list with a new fields-list
        newBoard.fields = newField
        return newBoard
    }

    /**
     * swaps the order in game.gameState.players(randomly)
     */
    fun shufflePlayers() {
        //Nicolas
        val gameState = rootService.game.currentGameState
        gameState.players.shuffle()
        onAllRefreshables { refreshAfterNetPlayersChanged() }
    }

    /**
     * swaps the position of player1 and player2
     *
     * this is a triangle swap.
     */
    fun flipPlayers(player1: Int, player2: Int) {
        val gameState = rootService.game.currentGameState
        val tempPlayer = gameState.players[player1]
        gameState.players[player1] = gameState.players[player2]
        gameState.players[player2] = tempPlayer
    }

    /**
     * swaps players, so staht ther first player is ath the position of the first number in the given list
     */
    fun orderPlayers(list : List<Int>) {
        val gameState = rootService.game.currentGameState
        var playerList = gameState.players.zip(list)
        playerList = playerList.sortedWith(compareBy { it.second })
        gameState.players = playerList.map { it.first }.toMutableList()


        onAllRefreshables { refreshAfterNetPlayersChanged() }
    }

    /**
     * This method increases the currentPlayer and gives them one remaining round
     */
    fun setUpNextRound() {
        println("SetUpNextRound:")

        val gameState = rootService.game.currentGameState
        gameState.currentPlayerIndex = (gameState.currentPlayerIndex + 1) % gameState.players.size
        gameState.players[gameState.currentPlayerIndex].remainingRounds = 1

        //set NetworkState
        if (gameState.players[gameState.currentPlayerIndex].type == PlayerType.LOCAL) {
            rootService.networkService.updateConnectionState(ConnectionState.PLAYING_MY_TURN)
        } else {
            rootService.networkService.updateConnectionState(ConnectionState.WAITING_FOR_OPPONENT_TURNS)
        }
        //new State to work on
        //here will all placeTile happen (play)
        rootService.game.createNextGameState()
        BoardGameApplication.runOnGUIThread {
            onAllRefreshables { refreshAfterTurn() }
        }

        //gameState = rootService.game.currentGameState
        // if the now current player is an AI. Make an AI move
        /*if(gameState.players[gameState.currentPlayerIndex].type == PlayerType.AI) {
            println("Calling AI::")
            println(rootService.game.gameStateList.size)
            rootService.aiService.makeMove()
        } else if(gameState.players[gameState.currentPlayerIndex].type == PlayerType.AI_RANDOM) {
            rootService.aiRandomService.makeMove()
        } else {
            println("Did not call an ai")
        }*/
    }
}