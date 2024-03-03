package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*
import kotlin.math.abs

/**
 * Test class for the [Board] entity.
 */
internal class BoardTest {

    /**
     * The initTest tests the initialization of the board. The board is sized differently depending on the count of
     * players. There are also start colors at specific locations on the board.
     * With this test, we actually also test the get column/row range functions. So we don't need to test them later.
     */
    @Test
    fun initTest() {
        // Let's start by creating a board for two players. Only the innermost (white) area of the board should be used.
        // This translates to a board of the size 11 x 11 hexagons (measured at the center point (0,0))
        // Then we increment the radius and player count by one and test again.
        for (radius in 5..7) {
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            // Now we can test the size. Let's test every row and column. It is a bit tedious, but it will give us more
            // test coverage.
            // testing the columns:
            for (column in -radius..radius) {
                val columnRage = board.getColumnRange(column)
                if (column <= 0) {
                    // abs(row)-radius and radius-row gives us exactly the min/max column position of the column
                    assertEquals(abs(column) - radius, columnRage.first)
                    assertEquals(radius, columnRage.second)
                } else {
                    // for positive rows it is reversed
                    assertEquals(-radius, columnRage.first)
                    assertEquals(radius - column, columnRage.second)
                }
            }
            // testing the rows:
            for (row in -radius..radius) {
                val rowRange = board.getRowRange(row)
                if (row <= 0) {
                    // abs(row)-radius and radius-row gives us exactly min/max row position of the row
                    assertEquals(abs(row) - radius, rowRange.first)
                    assertEquals(radius, rowRange.second)
                } else {
                    // for positive rows it is reversed
                    assertEquals(-radius, rowRange.first)
                    assertEquals(radius - row, rowRange.second)
                }
            }
            // now we just need to check if the start tiles are in the right position and are different.
            val startHexagons = arrayOf(
                board.getTileColor(0, -5),
                board.getTileColor(5, -5),
                board.getTileColor(5, 0),
                board.getTileColor(0, 5),
                board.getTileColor(-5, 5),
                board.getTileColor(-5, 0)
            )
            for (startHex in startHexagons) {
                // test if the tile has a color:
                assertTrue(startHex != TileColor.OUT_OF_BOARD && startHex != TileColor.EMPTY)
            }
            // test if they are unique by using a set
            assertTrue(startHexagons.size == startHexagons.toSet().size)
            // let's check if all empty and out of board fields are set correctly
            testFields(board, fields, radius)
            println("Done testing for radius $radius")
        }
    }

    //This method is used in the init test. It tests the empty and out of board fields
    private fun testFields(board: Board, fields: java.util.ArrayList<java.util.ArrayList<TileColor>>, radius: Int) {
        for (row in -radius..radius) {
            for (column in -radius..radius) {
                // continue if the field is a start field
                if ((row in arrayOf(-5, 5, 0)) && (column in arrayOf(-5, 5, 0)))
                    continue
                // otherwise we need to check the hexagon
                // first case: the hexagon is in the game
                if ((column >= board.getRowRange(row).first && column <= board.getRowRange(row).second) &&
                    (row >= board.getColumnRange(column).first && row <= board.getColumnRange(column).second)
                ) {
                    assertTrue(fields[column + 7][row + 7] == TileColor.EMPTY)
                } else {
                    // second case: the hexagon is not in the game:
                    assertTrue(fields[column + 7][row + 7] == TileColor.OUT_OF_BOARD)
                }
            }
        }
    }

    @Test
    fun getLineLength() {
        //Nicolas
        //this board does not need any specific sizes/parameters
        val fields = ArrayList<ArrayList<TileColor>>()
        var board = Board(5,fields,2)
        val orientationSet = TileOrientation.values()
        val colorSet = TileColor.values()

        //test, if the empty board has no lines of any Color
        //for every color
        for(color in colorSet){
            if(color != TileColor.OUT_OF_BOARD){
                for(orientation in orientationSet){
                    board.fields[board.indexToRealIndex(0,0).first][board.indexToRealIndex(0,0).second] = color
                    if(color == TileColor.EMPTY){

                        assertEquals(4,board.getLineLength(0,0,orientation))
                    }
                    else{
                        assertEquals(0,board.getLineLength(0,0,orientation))
                    }
                }
            }
        }

        //check if it can detect the edges
        //using the start tile RED at -5/0 as example
        board = Board(5,fields,2)
        for(orientation in orientationSet){
            assertEquals(0,board.getLineLength(-5,0,orientation))
        }

        //check if the method can detect a line starting from red to
        for(i in 0 .. 3){
            fields[board.indexToRealIndex((-5+i),0).first][board.indexToRealIndex(-5+i,0).second] = TileColor.RED
        }
        assertEquals(3,board.getLineLength(-5,0,TileOrientation.DOWN_RIGHT))
    }

    @Test
    fun isInGameBoard() {
        //Nicolas
        //doing the test for every radius
        for (radius in 5..7) {
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            //test for -7 to 7 since these are the tiles for the biggest game
            for (column in -7..7) {
                for (row in -7..7) {
                    assertEquals(board.getTileColor(column,row) != TileColor.OUT_OF_BOARD, board.isInGameBoard(column,row))
                }
            }
        }
    }

    @Test
    fun isFull() {
        //Nicolas
        //test if an empty board is not full
        for(radius in 5..7){
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            assertEquals(false,board.isFull())
        }

        //test for a full board
        for (radius in 5..7){
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            //fill the board
            for (column in -radius..radius) {
                for (row in -radius..radius) {
                    val colorToSet = TileColor.values().dropLast(2).random()
                    fields[board.indexToRealIndex(column,row).first][board.indexToRealIndex(column,row).second] = colorToSet
                }
            }
            //println("radius: $radius")
            assertTrue(board.isFull())
        }

        //test if the field is almost full
        for (radius in 5..7){
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            //fill the board
            for (column in -radius..radius) {
                for (row in -radius..radius) {
                    //drop adding the last few new tiles right at the end of filling the Board
                    if(row < -1 && column == board.radius){
                        break
                    }
                    val colorToSet = TileColor.values().dropLast(2).random()
                    fields[board.indexToRealIndex(column,row).first][board.indexToRealIndex(column,row).second] = colorToSet
                    assertFalse(board.isFull())
                }
            }
            //println("radius: $radius")

        }

    }

    @Test
    fun getTileColor() {
        // Doing the test for every radius
        for (radius in 5..7) {
            val fields = ArrayList<ArrayList<TileColor>>()
            val board = Board(radius, fields, radius - 3)
            for (column in -radius..radius) {
                for (row in -radius..radius) {
                    // fill the array with random tile colors
                    val realIndex = board.indexToRealIndex(column, row)
                    val colorToSet = TileColor.values().dropLast(1).random()
                    fields[realIndex.first][realIndex.second] = colorToSet
                    println("Set hexagon (${realIndex.first}|${realIndex.second}) " +
                            "to ${fields[realIndex.first][realIndex.second]}")
                    // retrieve the tile colors
                    assertEquals(colorToSet.ordinal, board.getTileColor(column,row).ordinal)
                }
            }
        }
    }

    @Test
    fun indexToRealIndex() {
        //checkin every field for every radius
        for (radius in 5..7) {
            val board = Board(radius, ArrayList(), radius - 3)
            for (column in -radius..radius) {
                for (row in -radius..radius) {
                    val realIndex = board.indexToRealIndex(column, row)
                    assertEquals(column + 7, realIndex.first)
                    assertEquals(row + 7, realIndex.second)
                }
            }
        }
    }
}
