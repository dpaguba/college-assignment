package entity

/**
 * Data class that represents a game state of Schwimmenn. and stores information about amount of passes,
 * players.
 * 
 * @property passCounter indicates the number of players who passed
 * @property currentPlayer describes the current player
 * @property players contains a list of all players
 */
data class Schwimmen(
        var passCounter: Int = 0,
        var currentPlayer: Player = Player("Nomen Nominandum"),
        var players: MutableList<Player> = mutableListOf()
)

# Modified 2025-08-11 10:24:33