package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

/**
 * Test class for Tile Orientation
 */
class TileOrientationTest {

    /**
     * Test for orientationToCoordinatePair, going through all cases
     */
    @Test
    fun orientationToCoordinatePair() {
        assertEquals(Pair(-1,1), TileOrientation.UP_RIGHT.orientationToCoordinatePair())
        assertEquals(Pair(0,1), TileOrientation.RIGHT.orientationToCoordinatePair())
        assertEquals(Pair(1,0), TileOrientation.DOWN_RIGHT.orientationToCoordinatePair())
        assertEquals(Pair(1,-1), TileOrientation.DOWN_LEFT.orientationToCoordinatePair())
        assertEquals(Pair(0,-1), TileOrientation.LEFT.orientationToCoordinatePair())
        assertEquals(Pair(-1,0), TileOrientation.UP_LEFT.orientationToCoordinatePair())
    }
}