package entity

import kotlinx.serialization.Serializable

/**
 * Represents a player in a game.
 * @param name The name of the player.
 * @param type The type of the player (e.g., human or AI).
 */
@Serializable
data class Player (val name : String, val type : PlayerType){
    /**
     * Indicates whether the player is in the first round.
     */
    var isInFirstRound : Boolean = true

    /**
     * Indicates how many rounds the player has.
     */
    var remainingRounds : Int = 0

    /**
     * The scoreboard of the player.
     */
    var scoreBoard : MutableMap <TileColor, Int> = mutableMapOf(
        Pair(TileColor.RED, 0),
        Pair(TileColor.YELLOW, 0),
        Pair(TileColor.GREEN, 0),
        Pair(TileColor.PURPLE, 0),
        Pair(TileColor.ORANGE, 0),
        Pair(TileColor.BLUE, 0)
    )

    /**
     * The list of tiles.
     */
    var rack = mutableListOf<Tile>()

    /**
     * Checks if the player's rack is swappable.
     * @return `true` if the rack is swappable, `false` otherwise.
     */
    fun rackIsSwappable() : Boolean{
        val minColors = findMinKeys()

        for(color in minColors){
            for (tile in rack){
                if (color == tile.firstColor || color == tile.secondColor){
                    return false
                }
            }
        }
        return true
    }

    /**
     * Finds the TileColor keys associated with the minimum values in the scoreBoard.
     * @return A list of TileColor keys with the minimum values.
     */
    private fun findMinKeys() : List<TileColor>{
        val minValues = scoreBoard.values.minOrNull() ?: return emptyList()
        return scoreBoard.filter { it.value == minValues }.keys.toList()
    }
}