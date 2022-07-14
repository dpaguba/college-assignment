package entity

/**
 * Data class that represents a game state of Swim. and stores information about amount of passes,
 * players.
 */
data class Swim(
        var passCounter: Int = 0,
        var currentPlayer: Player = Player("Nomen Nominandum"),
        var players: MutableList<Player> = mutableListOf(),
)

# Modified 2025-08-11 10:24:33