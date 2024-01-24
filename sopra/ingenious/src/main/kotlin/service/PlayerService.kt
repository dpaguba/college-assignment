package service

import entity.*

/**
 * Service class for player-related actions in the game "Ingenious".
 * @property rootService The root service which manages all services and has the connection to the entity layer
 */
class PlayerService(val rootService: RootService) : AbstractRefreshingService() {
    /**
     * Main player-action to place [Tile]s on the [Board].
     * The [Player] chooses a [Tile] from his rack, and then chooses the position on the [Board]. This method checks if
     * the positioning is legal and then calls [updateScoreboard] to refresh the scoreboard of the current [Player] and
     * then calls [GameService.finishTurn] from the [GameService] to end his turn.
     * @param tileOnRack The [Tile] on rack, which is supposed to be placed
     * @param column The desired column on the [Board] on which the [Player] wants to place his tile
     * @param row The desired row on the [Board] on which the [Player] wants to place his tile
     * @param orientation The orientation of the [Tile]: RIGHT, UP_RIGHT, DOWN_RIGHT, LEFT, UP_LEFT or DOWN_LEFT
     */
    fun placeTile(tileOnRack: Int, column: Int, row: Int, orientation:TileOrientation){
        // Retrieving the current gameState
        val gameState = rootService.game.currentGameState
        val currentPlayerIndex = gameState.currentPlayerIndex
        val board = gameState.board

        if(tileOnRack >= gameState.players[currentPlayerIndex].rack.size){
            throw IllegalArgumentException("Illegal tileIndex chosen, rack is not full!")
        }

        // Checking if an allowed column/row has been selected
        if (kotlin.math.abs(row) > 7 || kotlin.math.abs(column) > 7){
            throw IllegalArgumentException("Illegal column/row submitted! Only allowed: -7 to 7")
        }

        // Checking if an empty field was selected
        if (board.getTileColor(column, row) != TileColor.EMPTY){
            if (board.getTileColor(column, row) == TileColor.OUT_OF_BOARD){
                throw IllegalArgumentException("Cannot place tile out of board!")
            } else {
                throw IllegalArgumentException("Cannot place tile on an already existing color!")
            }
        }

        // calculate the offset of the orientation/direction of the Tile
        val orientOffset : Pair<Int,Int> = orientation.orientationToCoordinatePair()

        // Checking if the second selected field is also empty
        if (board.getTileColor(column + orientOffset.first, row + orientOffset.second) != TileColor.EMPTY){
            if (board.getTileColor(column + orientOffset.first, row + orientOffset.second) ==
                TileColor.OUT_OF_BOARD){
                throw IllegalArgumentException("Cannot place tile out of board!")
            } else {
                throw IllegalArgumentException("Cannot place tile on an already existing color!")
            }
        }
        // In First Round: Checking if placed tile is adjacent to an unoccupied starting color symbol. If not,
        // return and prompt player to choose a valid position
        if (gameState.players[currentPlayerIndex].isInFirstRound){
            if (isPlacedToNewStartSymbol(column,row, orientation)){
                gameState.players[currentPlayerIndex].isInFirstRound = false
            } else {
                throw IllegalArgumentException("First Round! Tile has to be placed next to an unoccupied starting " +
                        "color symbol!")
            }
        }
        // Board is populated with the colors of the tile
        setColorOnField(column, row, gameState.players[currentPlayerIndex].rack[tileOnRack].firstColor)
        setColorOnField(column + orientOffset.first, row + orientOffset.second,
            gameState.players[currentPlayerIndex].rack[tileOnRack].secondColor)
        //sending the place message
        if(rootService.game.isNetworkGame && gameState.players[currentPlayerIndex].type != PlayerType.NETWORK){
            rootService.networkService.sendIngeniousPlaceMessage(
                gameState.players[currentPlayerIndex].rack[tileOnRack].firstColor,
                gameState.players[currentPlayerIndex].rack[tileOnRack].secondColor,
                column,row,
                column + orientOffset.first,row + orientOffset.second,)
            println("Placed at: $row,$column, with color " +
                    "${gameState.players[currentPlayerIndex].rack[tileOnRack].firstColor}")
        }
        // remove the tile on the current players rack
        gameState.players[currentPlayerIndex].rack.removeAt(tileOnRack)

        //  Scoreboard is now updated
        updateScoreboard(column, row,orientation)

        // Turn is concluded and a bonus round might be triggered after
        rootService.gameService.finishTurn()
    }

    /**
     * Player-Action to swap the current [Player]s rack, if possible. Only allowed if the current [Player] has no
     * [Tile]s of his lowest ranking color on his rack.
     */
    fun swapRack(){
        // retrieve gameState
        val gameState = rootService.game.currentGameState
        val currentPlayer = gameState.players[gameState.currentPlayerIndex]
        val rack = currentPlayer.rack
        val bag = gameState.bag
        val removedTiles = mutableListOf<Tile>()

        if (currentPlayer.rackIsSwappable()){
            // remove tiles from current rack
            repeat(rack.size){
                removedTiles.add(rack.removeFirst())
            }

            repeat(6){
                rack.add(bag.removeLast())
            }

            // add removed tile back into the bag
            bag.addAll(removedTiles)

            bag.shuffle()
            if(rootService.game.isNetworkGame && gameState.players[gameState.currentPlayerIndex].type !=
                PlayerType.NETWORK){
                rootService.networkService.sendIngeniousEndTurnMessage(
                    swapAllFlag = true,
                    gameEnded = false,
                    firstBag = bag
                )
            }
        } else {
            throw IllegalArgumentException("Rack is not swappable!")
        }
        // set up the next round
        rootService.gameService.setUpNextRound()
    }

    /**
     * Called by [placeTile], to update the current [Player]s Scoreboard, it calculates the points of the newly placed
     * [Tile]. It checks every direction, and by that calculates the points for each line by calling the recursive
     * method [Board.getLineLength]
     * @param column The column of the placed [Tile]
     * @param row The row of the placed [Tile]
     * @param orientation The orientation of the [Tile]
     */
    private fun updateScoreboard(column: Int, row: Int, orientation: TileOrientation){
        // retrieve current gameState from rootService
        val gameState = rootService.game.currentGameState

        // retrieve currentPlayer, board and scoreBoard from gameState
        val currentPlayer = gameState.players[gameState.currentPlayerIndex]
        val board = gameState.board
        val scoreBoard = currentPlayer.scoreBoard

        // Check the current players scoreboard for colors that have already reached 18 or 36 points before
        val finishedColors = ArrayList<TileColor>()
        for (colors in scoreBoard){
            if (colors.value >= 18 && !rootService.game.isTeamMode){
                finishedColors.add(colors.key)
            }
            if (colors.value >= 36 && rootService.game.isTeamMode){
                finishedColors.add(colors.key)
            }
        }

        // Color of first Tile
        val colorFirstTile = board.getTileColor(column,row)

        //count points in every direction (except the line the tile sits on) for first tile part
        for (direction in TileOrientation.values()){
            if (direction != orientation && direction != getReversedLine(orientation)){
                val addedPoints = board.getLineLength(column,row,direction)

                scoreBoard[colorFirstTile] = scoreBoard[colorFirstTile]!! + addedPoints
            }
        }

        // Offset and color of the second tile
        val secOffset = orientation.orientationToCoordinatePair()
        val colorSecondTile = board.getTileColor(column + secOffset.first, row + secOffset.second)

        //count points in every direction (except the line the tile sits on) for second tile part
        for (direction in TileOrientation.values()){
            if (direction != orientation && direction != getReversedLine(orientation)){
                val addedPoints = board.getLineLength(column + secOffset.first,
                    row + secOffset.second,direction)

                scoreBoard[colorSecondTile] = scoreBoard[colorSecondTile]!! + addedPoints
            }
        }

        // count points for remaining directions
        val addRevPoints = board.getLineLength(column,row,getReversedLine(orientation))
        scoreBoard[colorFirstTile] = scoreBoard[colorFirstTile]!! + addRevPoints

        val addOrientPoints = board.getLineLength(column + secOffset.first,
            row + secOffset.second,orientation)
        scoreBoard[colorSecondTile] = scoreBoard[colorSecondTile]!! + addOrientPoints

        // change the current players round count to the count of colors that have reached 18 or 36 points
        var bonusCounter = 0
        for (colors in scoreBoard){
            if (!finishedColors.contains(colors.key)){
                if (colors.value >= 18 && !rootService.game.isTeamMode){
                    bonusCounter++
                }
                if (colors.value >= 36 && rootService.game.isTeamMode){
                    bonusCounter++
                }
            }
        }
        currentPlayer.remainingRounds += bonusCounter
    }

    /**
     * Returns the reversed line
     * @param orientation the orientation that has to be reversed
     * @return The reversed orientation
     */
    fun getReversedLine(orientation: TileOrientation):TileOrientation{
        return when (orientation){
            TileOrientation.RIGHT -> TileOrientation.LEFT
            TileOrientation.LEFT -> TileOrientation.RIGHT
            TileOrientation.UP_RIGHT -> TileOrientation.DOWN_LEFT
            TileOrientation.DOWN_LEFT -> TileOrientation.UP_RIGHT
            TileOrientation.DOWN_RIGHT -> TileOrientation.UP_LEFT
            TileOrientation.UP_LEFT -> TileOrientation.DOWN_RIGHT
        }
    }

    /**
     * Action which is called by [GameService.finishTurn] to fill the rack after the [Player] has placed a [Tile]
     */
    fun fillRack(){
        println("fill Rack:")
        val gameState = rootService.game.currentGameState
        val currentPlayer = gameState.players[gameState.currentPlayerIndex]
        val rack = currentPlayer.rack
        val bag = gameState.bag

        while (rack.size < 6){
            rack.add(bag.removeLast())
        }

        if(rootService.game.isNetworkGame&&gameState.players[gameState.currentPlayerIndex].type != PlayerType.NETWORK){
            rootService.networkService.sendIngeniousEndTurnMessage(
                swapAllFlag = false,
                gameEnded = false,
                firstBag = bag
            )
        }
        // set up the next round
        rootService.gameService.setUpNextRound()
    }

    /**
     * Only in first Round: Checks if the placed tile is adjacent to a new start symbol
     * @param column The column of the tile
     * @param row The row of the tile
     * @param orientation The orientation of the tile
     * @return Return true, if it has found a neighbouring start symbol, which still has no neighbours
     */
    fun isPlacedToNewStartSymbol(column: Int, row: Int, orientation: TileOrientation): Boolean {
        // check first field if it has a connection to a start field
        if (checkDirectionsForStartField(column, row)){
            return true
        }

        // check second field if it has a connection to a start field
        val orientOff = orientation.orientationToCoordinatePair()
        if (checkDirectionsForStartField(column + orientOff.first, row + orientOff.second)){
            return true
        }

        // no connection found
        return false
    }

    /**
     * Checks every direction for a start symbol and returns true if it is not already adjacent to an already placed
     * tile
     * @param column Column of the field
     * @param row Row of the field
     * @return Returns true if it found a still not connected Start Field
     */
    private fun checkDirectionsForStartField(column: Int, row: Int):Boolean{
        val gameState = rootService.game.currentGameState

        // check if legal arguments have been submitted
        if (kotlin.math.abs(column) > 7 || kotlin.math.abs(row) > 7){
            throw IllegalArgumentException("Illegal Row/Column Submitted!")
        }

        // check if it's still on the board
        if (gameState.board.getTileColor(column, row) == TileColor.OUT_OF_BOARD){
            throw IllegalArgumentException("position out of board!")
        }

        // Coordinates of the start symbols
        val redStart = Pair(-5,0)
        val greenStart = Pair(-5,5)
        val blueStart = Pair(0,5)
        val orangeStart = Pair(5,0)
        val yellowStart = Pair(5,-5)
        val purpleStart = Pair(0,-5)

        // check every direction for a start field, if found check if it's still free
        for (direction in TileOrientation.values()){
            val dirOffset = direction.orientationToCoordinatePair()

            //check current direction for a start field, then check if it already has a neighbour
            when (Pair(column + dirOffset.first, row + dirOffset.second)){
                redStart -> return !hasANeighbour(redStart.first, redStart.second)
                greenStart -> return !hasANeighbour(greenStart.first, greenStart.second)
                blueStart -> return !hasANeighbour(blueStart.first, blueStart.second)
                orangeStart -> return !hasANeighbour(orangeStart.first, orangeStart.second)
                yellowStart -> return !hasANeighbour(yellowStart.first,yellowStart.second)
                purpleStart -> return !hasANeighbour(purpleStart.first,purpleStart.second)
            }
        }
        // no start field found
        return false
    }

    /**
     * Checks, if a field on the [Board] has a Neighbour (another color than EMPTY or OUT_OF_BOARD)
     * @param column The column of the field
     * @param row The row of the field
     * @return a Boolean to indicate if a neighbour has been found
     */
    fun hasANeighbour(column: Int, row: Int): Boolean{
        val gameState = rootService.game.currentGameState

        // Check if the current field is still inside the board
        if (!gameState.board.isInGameBoard(column,row)){
            throw IllegalArgumentException("Cannot check an field which is out of Board!")
        }

        // Check all directions for an already existing color which is not EMPTY
        for (direction in TileOrientation.values()){
            val dirOffset = direction.orientationToCoordinatePair()

            // Check if the next field is still inside the board
            if (gameState.board.isInGameBoard(column + dirOffset.first,row + dirOffset.second)){
                // found an already existing color -> Neighbour exists
                if (gameState.board.getTileColor(column + dirOffset.first, row + dirOffset.second) !=
                    TileColor.EMPTY){
                    return true
                }
            }
        }

        // went through all direction and no neighbour has been found
        return false
    }

    /**
     * Sets a color on a field Neighbour
     * @param column The column of the field
     * @param row The row of the field
     * @param color The desired color which will be placed on the field
     */
    fun setColorOnField(column: Int, row: Int, color: TileColor){
        val gameState = rootService.game.currentGameState
        val pos = gameState.board.indexToRealIndex(column, row)

        gameState.board.fields[pos.first][pos.second] = color
    }
}