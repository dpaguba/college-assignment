package entity

import kotlinx.serialization.Serializable

/**
 * Enum to understand where was the tile placed:
 * up-right, right, down-right, down-left, left, up-left
 * */
@Serializable
enum class TileOrientation {
    UP_RIGHT,
    RIGHT,
    DOWN_RIGHT,
    DOWN_LEFT,
    LEFT,
    UP_LEFT;

    /**
     * The method returns the X and Y shift to perform in order to go one tile in the [TileOrientation]s direction.
     * Use .first as X and .second as Y
     *
     * @return Pair of Int first is X and second is Y
     * @see [Hexagon Grid Doku](https://tudo-aqua.github.io/bgw/components/container/container.html#hexagongrid)
     */
    fun orientationToCoordinatePair(): Pair<Int, Int> {
        return when(this) {
            UP_RIGHT -> Pair(-1,1)
            RIGHT -> Pair(0,1)
            DOWN_RIGHT -> Pair(1,0)
            DOWN_LEFT -> Pair(1,-1)
            LEFT -> Pair(0,-1)
            UP_LEFT -> Pair(-1,0)
        }
    }
}
# Modified 2025-08-11 10:24:31