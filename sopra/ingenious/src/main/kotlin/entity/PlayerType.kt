package entity

import kotlinx.serialization.Serializable

/**
 * Enum to distinguish between player's type:
 * artificial intelligence (ai), network, local
 * */
@Serializable
enum class PlayerType {
    AI,
    AI_RANDOM,
    NETWORK,
    LOCAL,
    ;
}
