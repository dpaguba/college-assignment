package entity

import kotlinx.serialization.Serializable

/**
 * The game state is the current state of the game. It can be used as al linked list.
 *
 * @param currentPlayerIndex is per default 0
 * @param prevGameState is the GameState before this one
 * @param nextGameState is the GameState after this one
 * @param bag is a list of [Tile]s
 * @param players is a list of [Player]s
 * @param board is the game [Board]
 */
@Serializable
data class GameState(
    var currentPlayerIndex: Int = 0,
    var prevGameState: GameState?,
    var nextGameState: GameState?,
    var bag: MutableList<Tile>,
    var players: MutableList<Player>,
    var board: Board
    )