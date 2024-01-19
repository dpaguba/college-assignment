package service

import entity.*
import view.Refreshable
import kotlin.random.Random

/**
 * The AI Service of the Ingenious Game, this class contains methods to follow a certain strategy, its strategy is
 * mainly focused to strengthen its own score and it not really playing against other players.
 * @property playerService The playerService with which, the aiService is directly connected, it calls the action of
 * placeTile
 * @property game The current game
 * @property rootService The rootService which is controlling all services, and it directly connected to the game
 * @property aiPlayer The current AI player
 * @property rack The rack of the current AI Player
 * @property scoreBoard The Scoreboard of the current AI Player
 * @property minBoardColor The minimum ranked color on the scoreboard
 */
class AiService(private val playerService: PlayerService) : Refreshable {
    private lateinit var game: Game
    private lateinit var rootService: RootService
    private lateinit var aiPlayer: Player
    private lateinit var rack: MutableList<Tile>
    private lateinit var scoreBoard: MutableMap<TileColor, Int>
    private lateinit var minBoardColor: Map.Entry<TileColor, Int>

    /**
     * Makes a move by evaluating possible actions and selecting the best move for the current game situation
     */
    fun makeMove() {
        // setting everything new in order to work on the newest data
        game = playerService.rootService.game
        rootService = playerService.rootService
        aiPlayer = game.currentGameState.players[game.currentGameState.currentPlayerIndex]
        rack = aiPlayer.rack
        scoreBoard = aiPlayer.scoreBoard
        minBoardColor = scoreBoard.minBy { it.value }

        /*if (aiPlayer.rack.size != 6) {
            // oh shit something is messed up. Play save. Do nothing
            println("AI did nothing since the rack is bad!\n Rack=${aiPlayer.rack}")
            return
        }*/
        val startTime = System.currentTimeMillis()
        val actionList: ArrayList<Action> = if (aiPlayer.isInFirstRound) {
            searchForFirstRoundAction()
        } else {
            searchForLegalAction()
        }

        if (actionList.size == 0) {
            // something is wrong. The game should have already been stopped...
            println("AI did nothing since there was no empty field!")
            return
        }

        aiPlayer.scoreBoard.toList().sortedBy { it.second }

        val moves = mutableListOf<AiMove>()

        // create an array of moves
        for ((actionId) in actionList.withIndex()) {
            // for each tile on rack
            for (tileOnRack in 0 until rack.size) {
                moves.add(AiMove(actionId, tileOnRack))
            }
        }
        // print the count of moves:
        println("wow. There are ${moves.size} possible moves!")

        // now we need to evaluate each move and give it a score.
        // a move score is a number. The higher, the better the move.
        for (move in moves) {
            evaluateMove(move, actionList)
        }

        // now we just need to perform the best scoring move:
        val bestMove = moves.maxBy { it.score }
        val timeOfCalculation = System.currentTimeMillis() - startTime
        // print the move that we are going to perform:
        println(
            "Doing move:\n" +
                    "\tCalculation time=${timeOfCalculation}ms\n" +
                    "\tAction=${bestMove.actionId}\n" +
                    "\t\t->${actionList[bestMove.actionId]}\n" +
                    "\ttile on rack=${bestMove.tileIndex}\n" +
                    "\t\t->${aiPlayer.rack[bestMove.tileIndex]}\n" +
                    "\tmove's score=${bestMove.score}\n"+
                    "\tmove quality=${(bestMove.score/251.0)*100.0}%\n"
        )
        val action = actionList[bestMove.actionId]
        playerService.placeTile(bestMove.tileIndex, action.column, action.row, action.orientation)
    }

    /**
     * This is the heart of the AI. It calculates a score for the move based on differently weighted properties.
     * @param move The move to evaluate
     * @param actions List of available actions
     */
    private fun evaluateMove(move: AiMove, actions: ArrayList<Action>) {
        // Place everything that should contribute to the moves' quality inside here
        //move.score = Random.nextInt() // just for testing

        // one or both colors have reached 18 subtract some points
        if(colorIsMaxInScoreBoard(rack[move.tileIndex].firstColor)){
            move.score -= 5
        }
        if(colorIsMaxInScoreBoard(rack[move.tileIndex].secondColor)){
            move.score -= 5
        }

        // If one of the tile colors is the lowest on the scoreboard: +10 points
        if (rack[move.tileIndex].firstColor == minBoardColor.key ||
            rack[move.tileIndex].secondColor == minBoardColor.key
        ) {
            move.score += 10
        }

        // Add the gained Points to score. This one has a weight: 0.5
        val gameScoresReachable = calculateScore(move.tileIndex, actions[move.actionId])
        move.score += ((gameScoresReachable.first + gameScoresReachable.second)*1)

        // if color is less than 40% than max on score board and points are reachable: +100 points
        val threshold = (scoreBoard.values.max()*0.6).toInt()
        if(scoreBoard.getValue(rack[move.tileIndex].firstColor) <= threshold){
            move.score += 100
        }
        if(scoreBoard.getValue(rack[move.tileIndex].secondColor) <= threshold){
            move.score += 100
        }

        // if a one of the colors of the tile is 0: +200
        if(scoreBoard.getValue(rack[move.tileIndex].firstColor) == 0){
            move.score += 100
        }
        if(scoreBoard.getValue(rack[move.tileIndex].secondColor) == 0){
            move.score += 100
        }

            // if a bonus round can be reached (with not too much overhead): +60 points
        val col1PointsOnBoard = scoreBoard.getValue(rack[move.tileIndex].firstColor) + gameScoresReachable.first
        val col2PointsOnBoard = scoreBoard.getValue(rack[move.tileIndex].secondColor) + gameScoresReachable.second
        var bestMax = 20
        var bestMin = 18
        if(game.isTeamMode){
            bestMax = 38
            bestMin = 36
        }
        if(col1PointsOnBoard in bestMin..bestMax){
            move.score += 60
        }
        if(col2PointsOnBoard in bestMin..bestMax){
            move.score += 60
        }

        // to add some fun. Add a bit of randomness
        move.score += Random.nextInt(5)
    }

    /**
     * Checks if the given tile color has already the maximum score on the scoreboard
     * @param tileColor The given tile color
     * @return True, if the colors score is greater than or equal to 18
     */
    private fun colorIsMaxInScoreBoard(tileColor: TileColor): Boolean {
        return 18 <= scoreBoard.getValue(tileColor)
    }

    /**
     * Searches for legal actions that can be performed on the game board.
     * @return List of valid actions
     */
    private fun searchForLegalAction(): ArrayList<Action> {
        val gameState = playerService.rootService.game.currentGameState
        val board = gameState.board

        // start position: highest column
        var column = board.getRowRange(0).first

        // Offsets of each direction
        val rightOff = TileOrientation.RIGHT.orientationToCoordinatePair()
        val downRightOff = TileOrientation.DOWN_RIGHT.orientationToCoordinatePair()
        val downLeftOff = TileOrientation.DOWN_LEFT.orientationToCoordinatePair()

        val actionList = arrayListOf<Action>()

        // going through each row in each column, for example first: column -5: from row 0 to 5
        // and then column -4: from row -1 to 5, checking three direction DOWN_RIGHT,DOWN_LEFT and RIGHT
        while (column <= board.getRowRange(0).second) {
            for (row in board.getColumnRange(column).first..board.getColumnRange(column).second) {
                // CHECK OF RIGHT FIELD:
                if (board.isInGameBoard(column + rightOff.first, row + rightOff.second)) {
                    if (board.getTileColor(column, row) == TileColor.EMPTY &&
                        board.getTileColor(column + rightOff.first, row + rightOff.second) ==
                        TileColor.EMPTY
                    ) {
                        actionList.add(Action(column, row, TileOrientation.RIGHT))
                        actionList.add(Action(column + rightOff.first, row + rightOff.second,
                            TileOrientation.LEFT))
                    }
                }

                // CHECK OF RIGHT_DOWN FIELD
                if (board.isInGameBoard(column + downRightOff.first, row + downRightOff.second)) {
                    if (board.getTileColor(column, row) == TileColor.EMPTY &&
                        board.getTileColor(column + downRightOff.first, row + downRightOff.second) ==
                        TileColor.EMPTY
                    ) {
                        actionList.add(Action(column, row, TileOrientation.DOWN_RIGHT))
                        actionList.add(
                            Action(
                                column + downRightOff.first, row + downRightOff.second,
                                TileOrientation.UP_LEFT
                            )
                        )
                    }
                }

                // CHECK OF LEFT_DOWN FIELD
                if (board.isInGameBoard(column + downLeftOff.first, row + downLeftOff.second)) {
                    if (board.getTileColor(column, row) == TileColor.EMPTY &&
                        board.getTileColor(column + downLeftOff.first, row + downLeftOff.second) ==
                        TileColor.EMPTY
                    ) {
                        actionList.add(Action(column, row, TileOrientation.DOWN_LEFT))
                        actionList.add(
                            Action(
                                column + downLeftOff.first, row + downLeftOff.second,
                                TileOrientation.UP_RIGHT
                            )
                        )
                    }
                }
            }
            column++ // incrementing the column by 1, going from column -5 to 5 for example if players.size == 2
        }
        if (actionList.isEmpty()) {
            return arrayListOf()
            //throw Exception("Action list is empty, no free field found.")
        }

        return actionList
    }

    /**
     * Calculates the score achievable by placing a tile with this action on the game board
     * @param tileOnRack The index of the tile on the AI players rack.
     * @param action The action representing the tile placement on the board.
     * @return A Pair of Points: Pair(scoreFirstTile,scoreSecondTile)
     */

    private fun calculateScore(tileOnRack: Int, action: Action): Pair<Int, Int> {
        val gameState = playerService.rootService.game.currentGameState

        val column = action.column
        val row = action.row
        val orientation = action.orientation

        // retrieve currentPlayer, board and scoreBoard from gameState
        val currentPlayer = gameState.players[gameState.currentPlayerIndex]
        gameState.board

        var scoreFirstTile = 0
        var scoreSecondTile = 0

        // Color of first Tile
        val colorFirstTile = currentPlayer.rack[tileOnRack].firstColor

        //count points in every direction (except the line the tile sits on) for first tile part
        for (direction in TileOrientation.values()) {
            if (direction != orientation && direction != playerService.getReversedLine(orientation)) {
                scoreFirstTile += getLineLength(column, row, direction, colorFirstTile)

            }
        }

        // Offset and color of the second tile
        val secOffset = orientation.orientationToCoordinatePair()
        val colorSecondTile = currentPlayer.rack[tileOnRack].secondColor

        //count points in every direction (except the line the tile sits on) for second tile part
        for (direction in TileOrientation.values()) {
            if (direction != orientation && direction != playerService.getReversedLine(orientation)) {
                scoreSecondTile += getLineLength(
                    column + secOffset.first,
                    row + secOffset.second, direction, colorSecondTile
                )
            }
        }

        // count points for remaining directions
        scoreFirstTile += getLineLength(column, row, playerService.getReversedLine(orientation), colorFirstTile)

        scoreSecondTile += getLineLength(column + secOffset.first,
            row + secOffset.second, orientation, colorSecondTile)

        return Pair(scoreFirstTile, scoreSecondTile)
    }

    /**
     * Calculates the points for one line in the board, its calling itself recursive and stops if it does not find
     * another equal color
     * @param column The column on the board
     * @param row The row on the board
     * @param direction The direction which will be checked
     * @param color The color of the tile
     * @return Returns the score, generated in this line
     */
    private fun getLineLength(column: Int, row: Int, direction: TileOrientation, color: TileColor): Int {
        val board = playerService.rootService.game.currentGameState.board

        // help variable to determine the direction of the next tile
        val offset = direction.orientationToCoordinatePair()

        // check if next field is still inside the game
        if (!board.isInGameBoard(column + offset.first, row + offset.second)) {
            return 0
        }

        // check if the colors of the current and next tile are the same
        if (color != board.getTileColor(column + offset.first, row + offset.second)) {
            return 0
        }

        // 1 equal color found and keep on looking on the current line for more equal colors
        return 1 + getLineLength(
            column = column + offset.first, row = row + offset.second, direction = direction,
            color = board.getTileColor(column + offset.first, row + offset.second)
        )
    }

    /**
     * Searches specificly for first round actions, the ai has to place its tile next to a still unoccupied starting
     * symbol
     * @return Returns a list of all possible first round actions
     */
    private fun searchForFirstRoundAction(): ArrayList<Action> {
        val gameState = playerService.rootService.game.currentGameState
        val board = gameState.board
        val starts = arrayListOf(Pair(-5,0), Pair(-5,5), Pair(0,5), Pair(5,0), Pair(5,-5), Pair(0,-5))

        val freeStarts = arrayListOf<Pair<Int,Int>>()

        for (start in starts){
            if (!playerService.hasANeighbour(start.first, start.second)){
                freeStarts.add(start)
            }
        }

        val actionList = arrayListOf<Action>()

        for (start in freeStarts){
            // go the first field connected to the start field
            for (firstDir in TileOrientation.values()){
                val firstOff = firstDir.orientationToCoordinatePair()
                if (board.isInGameBoard(start.first + firstOff.first, start.second + firstOff.second)){
                    // Go to the second field, which is in the game board
                    for (secondDir in TileOrientation.values()){
                        if (secondDir != playerService.getReversedLine(firstDir)){
                            val secondOff = secondDir.orientationToCoordinatePair()
                            if (board.isInGameBoard(start.first + firstOff.first + secondOff.first,
                                    start.second + firstOff.second + secondOff.second)) {
                                actionList.add(Action(start.first + firstOff.first,
                                    start.second + firstOff.second, secondDir))
                                actionList.add(Action(start.first + firstOff.first + secondOff.first,
                                    start.second + firstOff.second + secondOff.second,
                                    playerService.getReversedLine(secondDir)))
                            }
                        }
                    }
                }
            }
        }

        return actionList
    }

    /**
     * Refreshes the ai if its rack is swappable, the ai does always swap if possible
     */
    override fun refreshAfterRackSwappable() {
        val playerIndex = playerService.rootService.game.currentGameState.currentPlayerIndex
        if(playerService.rootService.game.currentGameState.players[playerIndex].type == PlayerType.AI) {
            // For now, the AI will always swap
            println("Smart AI: swapping rack")
            playerService.swapRack()
        }
    }

    /**
     * Refreshes the ai, if it has reached a bonus round.
     */
    override fun refreshAfterBonusRound() {
        val gameState = playerService.rootService.game.currentGameState
        if (gameState.players[gameState.currentPlayerIndex].type == PlayerType.AI){
            makeMove()
        }
    }

    /**
     * Data class representation a possible move by the ai
     */
    data class AiMove(val actionId: Int, val tileIndex: Int, var score: Int = 0)

    /**
     * Data class representing a tile placement action
     * @property column The column on the board
     * @property row The row on the board
     * @property orientation The orientation of the tile in this action
     */
    data class Action(val column: Int, val row: Int, val orientation: TileOrientation)
}