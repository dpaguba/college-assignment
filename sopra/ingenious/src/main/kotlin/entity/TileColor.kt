package entity

import kotlinx.serialization.Serializable

/***
 * Enum to distinguish between tile colors:
 * red, green, blue, yellow, orange, purple, empty
 */
@Serializable
enum class TileColor{
    RED,
    GREEN,
    BLUE,
    YELLOW,
    ORANGE,
    PURPLE,
    EMPTY,
    OUT_OF_BOARD
    ;

}

# Modified 2025-08-11 10:24:31