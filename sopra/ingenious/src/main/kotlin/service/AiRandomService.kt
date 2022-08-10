package service

import entity.PlayerType
import entity.TileColor
import entity.TileOrientation
import view.Refreshable
import kotlin.random.Random

/**
 * Service class for the actions of a random ai, for testing reasons. It has a connection to the playerService and
 * makes moves, especially for testing reasons (no intelligence)
 * @property playerService The ai controls it own actions and calls placeTile with its own determined rackIndex,
 * column, row and orientation
 */
class AiRandomService(private val playerService: PlayerService): Refreshable {
    private var gameHasEnded = false
    /**
     * Main action of the ai, it chooses a random til from its rack, and then puts it on a random field
     */
    fun makeMove(){
        val gameState = playerService.rootService.game.currentGameState
        val aiPlayer = gameState.players[gameState.currentPlayerIndex]

        // ai randomly chooses a tile from its rack
        val tileOnRack = Random.nextInt(aiPlayer.rack.size)


        // create ai action
        val action = if (aiPlayer.isInFirstRound){
            searchForFirstRoundAction()
        } else {
            searchForLegalAction()
        }

        val column = action.first.first
        val row = action.first.second
        val orientation = action.second

        // Only for tests
        println("TileOnRack: $tileOnRack")
        println("column: $column")
        println("row: $row")
        println("orientation: $orientation")

        playerService.placeTile(tileOnRack, column,row,orientation)
    }

    /**
     * Searches for legal actions and then chooses one randomly
     * @return a Pair of the coordinates of column and row and of the orientation
     */
    private fun searchForLegalAction(): Pair<Pair<Int,Int>,TileOrientation>{
        val gameState = playerService.rootService.game.currentGameState
        val board = gameState.board

        // start position: uppest column
        var column = board.getRowRange(0).first

        // Offsets of each direction
        val rightOff = TileOrientation.RIGHT.orientationToCoordinatePair()
        val downRightOff = TileOrientation.DOWN_RIGHT.orientationToCoordinatePair()
        val downLeftOff = TileOrientation.DOWN_LEFT.orientationToCoordinatePair()

        val actionList = arrayListOf<Pair<Pair<Int,Int>, TileOrientation>>()

        // going through each row in each column, for example first: column -5: from row 0 to 5
        // and then column -4: from row -1 to 5, checking three direction DOWN_RIGHT,DOWN_LEFT and RIGHT
        while (column <= board.getRowRange(0).second){
            for (row in board.getColumnRange(column).first .. board.getColumnRange(column).second) {
                // CHECK OF RIGHT FIELD:
                if (board.isInGameBoard(column + rightOff.first, row + rightOff.second)) {
                    if (board.getTileColor(column,row) == TileColor.EMPTY &&
                        board.getTileColor(column + rightOff.first, row + rightOff.second) ==
                        TileColor.EMPTY
                    ) {
                        //return Pair(Pair(column,row), TileOrientation.RIGHT)
                        actionList.add(Pair(Pair(column,row), TileOrientation.RIGHT))
                    }
                }

                // CHECK OF RIGHT_DOWN FIELD
                if (board.isInGameBoard(column + downRightOff.first, row + downRightOff.second)) {
                    if (board.getTileColor(column,row) == TileColor.EMPTY &&
                        board.getTileColor(column + downRightOff.first, row + downRightOff.second) ==
                        TileColor.EMPTY
                    ) {
                        //return Pair(Pair(column,row), TileOrientation.DOWN_RIGHT)
                        actionList.add(Pair(Pair(column,row), TileOrientation.DOWN_RIGHT))
                    }
                }

                // CHECK OF LEFT_DOWN FIELD
                if (board.isInGameBoard(column + downLeftOff.first, row + downLeftOff.second)) {
                    if (board.getTileColor(column,row) == TileColor.EMPTY &&
                        board.getTileColor(column + downLeftOff.first, row + downLeftOff.second) ==
                        TileColor.EMPTY
                    ) {
                        //return Pair(Pair(column,row), TileOrientation.DOWN_LEFT)
                        actionList.add(Pair(Pair(column,row), TileOrientation.DOWN_LEFT))
                    }
                }
            }
            column++ // incrementing the column by 1, going from column -5 to 5 for example if players.size == 2
        }
        if (actionList.isEmpty()){
            throw IllegalStateException("No free Field found! Board has to be full!")
        }

        return actionList.random()
    }

    /**
     * Is called in first round, it searches for legal action and return of one them randomly
     * @return A pair of the legal action
     */
    private fun searchForFirstRoundAction():Pair<Pair<Int,Int>,TileOrientation>{
        val starts = arrayListOf(Pair(-5,0), Pair(-5,5), Pair(0,5), Pair(5,0), Pair(5,-5), Pair(0,-5))

        val actionList = arrayListOf<Pair<Pair<Int,Int>, TileOrientation>>()

        for (start in starts){
            if (!playerService.hasANeighbour(start.first, start.second)){
                when (start){
                    /*
                    Pair(-5,0) -> return Pair(Pair(-4,0), TileOrientation.DOWN_RIGHT) //red start
                    Pair(-5,5) -> return Pair(Pair(-4,4), TileOrientation.DOWN_LEFT) //green start
                    Pair(0,5) -> return Pair(Pair(-4,4), TileOrientation.LEFT) //blue start
                    Pair(5,0) -> return Pair(Pair(4,0), TileOrientation.UP_LEFT) //orange start
                    Pair(5,-5) -> return Pair(Pair(4,-4), TileOrientation.UP_RIGHT) //yellow start
                    Pair(0,-5) -> return Pair(Pair(0,-4), TileOrientation.RIGHT) //purple start
                    */
                    Pair(-5,0) -> actionList.add(Pair(Pair(-4,0), TileOrientation.DOWN_RIGHT)) //red start
                    Pair(-5,5) -> actionList.add(Pair(Pair(-4,4), TileOrientation.DOWN_LEFT)) //green start
                    Pair(0,5) -> actionList.add(Pair(Pair(0,4), TileOrientation.DOWN_RIGHT)) //blue start
                    Pair(5,0) -> actionList.add(Pair(Pair(4,0), TileOrientation.UP_LEFT)) //orange start
                    Pair(5,-5) -> actionList.add(Pair(Pair(4,-4), TileOrientation.UP_RIGHT)) //yellow start
                    Pair(0,-5) -> actionList.add(Pair(Pair(0,-4), TileOrientation.RIGHT)) //purple start
                }
            }
        }
        //throw IllegalStateException("No free Field adjacent to a start symbol found!")
        return actionList.random()
    }

    override fun refreshAfterRackSwappable() {
        // ai will always swap
        val playerIndex = playerService.rootService.game.currentGameState.currentPlayerIndex
        if(playerService.rootService.game.currentGameState.players[playerIndex].type == PlayerType.AI_RANDOM
            && !gameHasEnded){
            println("Random AI: swapping rack")
            playerService.swapRack()
            //playerService.fillRack()
        }
    }

    override fun refreshAfterBonusRound() {
        val gameState = playerService.rootService.game.currentGameState
        if(!gameHasEnded && gameState.players[gameState.currentPlayerIndex].type == PlayerType.AI_RANDOM){
            makeMove()
        }
    }

    override fun refreshAfterGameEnd(winner: String) {
        gameHasEnded = true
    }
}
# Modified 2025-08-11 10:24:31