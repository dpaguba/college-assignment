package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

/**
 * Test class for Tile
 */
class TileTest {
    private val tile = Tile(TileColor.PURPLE, TileColor.BLUE)
    /**
     * Test for getFirstColor
     */
    @Test
    fun getFirstColor() {
        assertEquals(TileColor.PURPLE, tile.firstColor)
        assertNotEquals(TileColor.BLUE, tile.firstColor)
    }

    /**
     * Test for getSecondColor
     */
    @Test
    fun getSecondColor() {
        assertEquals(TileColor.BLUE, tile.secondColor)
        assertNotEquals(TileColor.PURPLE, tile.secondColor)
    }
}