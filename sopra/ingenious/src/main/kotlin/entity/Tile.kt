package entity

import kotlinx.serialization.Serializable

/**
 * A tile is a compound of tow [TileColor]s. (two hexagons)
 *
 * @param firstColor is the color of the first part
 * @param secondColor is the color of the second part
 */
@Serializable
data class Tile(val firstColor: TileColor, val secondColor: TileColor)
# Modified 2025-08-11 10:24:31