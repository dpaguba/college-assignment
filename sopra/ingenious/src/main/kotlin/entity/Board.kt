package entity

import kotlinx.serialization.Serializable


/**
 * Class for the playing Board, it stores the colors of each tile placed on the board , it is also needed for
 * calculation of the score
 * @property radius Radius of the board
 * @property fields The fields on the board which have a certain color stored or are empty
 */
@Serializable
data class Board(
    var radius:Int,
    var fields: ArrayList<ArrayList<TileColor>> = ArrayList(),
    val playerSize: Int = 2 // hardcoded at the moment for testing reasons, normally currentGameState used
) {
    init{
        if (fields.isEmpty()){
            // Going through all possible column, pretending to initialize an 15x15 array
            for (column in -7 .. 7){
                val columnList = ArrayList<TileColor>()
                fields.add(columnList)
                val range = getColumnRange(column)
                // Going through all rows, pretending to init a 15 x 15 array, all field out of board get filled with
                // the color OUT_OF_BOARD
                for (row in -7 .. 7){
                    // Check if the row is still inside the game, if its not the field is filled with OUT_OF_BOARD
                    if (row >= range.first && row <= range.second){
                        columnList.add(TileColor.EMPTY)
                    } else {
                        columnList.add(TileColor.OUT_OF_BOARD)
                    }
                }
            }
            fields[indexToRealIndex(-5,0).first][indexToRealIndex(-5,0).second] = TileColor.RED
            fields[indexToRealIndex(-5,5).first][indexToRealIndex(-5,5).second] =
                TileColor.GREEN
            fields[indexToRealIndex(0,5).first][indexToRealIndex(0,5).second] = TileColor.BLUE
            fields[indexToRealIndex(5,0).first][indexToRealIndex(5,0).second] = TileColor.ORANGE
            fields[indexToRealIndex(5,-5).first][indexToRealIndex(5,-5).second] =
                TileColor.YELLOW
            fields[indexToRealIndex(0,-5).first][indexToRealIndex(0,-5).second] =
                TileColor.PURPLE
        }

    }
    /**
     * Recursive function to determine the length of the current line. Helpful for the calculation of the scoreboard
     * @param column The column of the current tile
     * @param row The row of the current tile
     * @param direction The Direction of the current line, which we are investigating
     * @return Returns the lineLength of the current Line. Important for the ScoreBoard
     */
    fun getLineLength(column: Int, row: Int, direction: TileOrientation):Int{
        // help variable to determine the direction of the next tile
        val offset = direction.orientationToCoordinatePair()

        // check if still inside the game
        if (!isInGameBoard(column + offset.first, row + offset.second)){
            return 0
        }
        // check if the colors of the current and next tile are the same
        if (getTileColor(column, row) != getTileColor(column + offset.first, row + offset.second)){
            return 0
        }

        // 1 equal color found and keep on looking on the current line for more equal colors
        return 1 + getLineLength(column + offset.first, row + offset.second, direction)
    }

    /**
     * Function to determine the Column Range of the indices of the submitted column
     * @param column The column on which we want to know the range
     * @return Return an Integer Pair of the Range, for example: Input column -1 :  (-4,5) means column -1 ranges from
     * row -4 to 5
     */
    fun getColumnRange(column: Int):Pair<Int,Int>{
        var range : Pair<Int,Int>

        if (column >= 6 || column <= -6 ){
            if (playerSize == 2)
            {
                return Pair(1,-1) // Return of an illegal value, cause first should always be smaller than second
            }

            if (column == 7 || column == -7){
                if (playerSize == 3){
                    return Pair(1,-1) // Return of an illegal value
                }
            }

            if (column > 7 || column < -7){
                return Pair(1,-1) // Return of an illegal value
            }
        }

        // Firstly calculation of the ranges of the indices of a small game board (2 players)
        range = if (column <= 0){
            Pair(-5 - column, 5)
        } else {
            Pair(-5, 5 - column)
        }

        // Editing the range, if the gameBoard is bigger: three players: shift by 1, four players: shift by 2
        if (playerSize == 3){
            range = Pair(range.first -1, range.second +1)
        } else if (playerSize == 4){
            range = Pair(range.first -2, range.second +2)
        }

        return range
    }

    /**
     * Function to determine the Row Range of the indices of the submitted row
     * @param row The row on which we want to know the range
     * @return Return an Integer Pair of the Range, for example: Input row -1 :  (-4,5) means row -1 ranges from
     * column -4 to 5
     */
    fun getRowRange(row: Int):Pair<Int,Int>{
        var range : Pair<Int,Int>

        if (row >= 6 || row <= -6 ){
            if (playerSize == 2)
            {
                return Pair(1,-1) // Return of an illegal value
            }

            if (row == 7 || row == -7){
                if (playerSize == 3){
                    return Pair(1,-1) // Return of an illegal value
                }
            }

            if (row > 7 || row < -7){
                return Pair(1,-1) // Return of an illegal value
            }
        }

        // Firstly calculation of the ranges of the indices of a small game board (2 players)
        range = if (row <= 0){
            Pair(-5 - row, 5)
        } else {
            Pair(-5, 5 - row)
        }

        // Editing the range, if the gameBoard is bigger: three players: shift by 1, four players: shift by 2
        if (playerSize == 3){
            range = Pair(range.first -1, range.second +1)
        } else if (playerSize == 4){
            range = Pair(range.first -2, range.second +2)
        }

        return range
    }

    /**
     * Determines if the submitted field is still in the current game board
     * @param column The column of the field
     * @param row The row of the field
     * @return Return true, if it still is in the board, and false if not
     */
    fun isInGameBoard(column: Int, row: Int): Boolean{
        // Alternative Version:
        /*if ((column > 7 || column < -7) || (row > 7 || row < -7)){
            return false
        }
        val index = indexToRealIndex(column,row)
        return fields[index.first][index.second] != TileColor.OUT_OF_BOARD*/

        if (column < getRowRange(row).first || column > getRowRange(row).second){
          return false
        }

        if (row < getColumnRange(column).first || row > getColumnRange(column).second){
            return false
        }

        return true
    }

    /**
     * Determines if the board is already full, which means there is no possible way of placing more tiles, even if
     * there is an individual remaining empty spot on the board
     * It goes through each column and checks there for each row each direction for two following empty fields
     * @return Return true if it is full
     */
    fun isFull(): Boolean{
        var column = getRowRange(0).first // start position up left in the board, going through each column

        // Directions
        val rightDir = TileOrientation.RIGHT
        val downRightDir =TileOrientation.DOWN_RIGHT
        val downLeftDir = TileOrientation.DOWN_LEFT

        // Offsets of each direction
        val rightOff = rightDir.orientationToCoordinatePair()
        val downRightOff = downRightDir.orientationToCoordinatePair()
        val downLeftOff = downLeftDir.orientationToCoordinatePair()

        // going through each row in each column, for example first: column -5: from row 0 to 5
        // and then column -4: from row -1 to 5, checking three direction DOWN_RIGHT,DOWN_LEFT and RIGHT
        while (column <= getRowRange(0).second){
            for (row in getColumnRange(column).first .. getColumnRange(column).second) {
                val currPos = indexToRealIndex(column, row) // Current Position

                // CHECK OF RIGHT FIELD:
                if (isInGameBoard(column + rightOff.first, row + rightOff.second)) {
                    // right Pos
                    val rightPos = indexToRealIndex(column + rightOff.first, row + rightOff.second)
                    if (fields[currPos.first][currPos.second] == TileColor.EMPTY &&
                        fields[rightPos.first][rightPos.second] == TileColor.EMPTY
                    ) {
                        return false
                    }
                }

                // CHECK OF RIGHT_DOWN FIELD
                if (isInGameBoard(column + downRightOff.first, row + downRightOff.second)) {
                    val downRightPos = indexToRealIndex(column + downRightOff.first,
                        row + downRightOff.second)
                    if (fields[currPos.first][currPos.second] == TileColor.EMPTY &&
                        fields[downRightPos.first][downRightPos.second] == TileColor.EMPTY
                    ) {
                        return false
                    }
                }

                // CHECK OF LEFT_DOWN FIELD
                if (isInGameBoard(column + downLeftOff.first, row + downLeftOff.second)) {
                    val downLeftPos = indexToRealIndex(column + downLeftOff.first,
                        row + downLeftOff.second)
                    if (fields[currPos.first][currPos.second] == TileColor.EMPTY &&
                        fields[downLeftPos.first][downLeftPos.second] == TileColor.EMPTY
                    ) {
                        return false
                    }
                }
            }
            column++ // incrementing the column by 1, going from column -5 to 5 for example if players.size == 2
        }

        return true // went through all fields and no fillable space found
    }


    /**
     * Retrieves the colour of the tile with its corresponding column and row index.
     */
    fun getTileColor(column: Int, row: Int) : TileColor{
        return fields[indexToRealIndex(column,row).first][indexToRealIndex(column,row).second]
    }

    /**
     * Gets a index from (7,-7) to (-7,7) and transfers it to the real index needed for the array. Because of negative
     * Indexes
     */
    fun indexToRealIndex(column: Int, row: Int): Pair<Int,Int>{
        if (column > 7 || column < -7){
            throw IllegalArgumentException("Illegal Column submitted")
        } else  if (row > 7 || row < -7){
            throw IllegalArgumentException("Illegal Row submitted")
        }
        return Pair(column + 7, row + 7)
    }
}

# Modified 2025-08-11 10:24:31