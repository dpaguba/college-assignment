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

# Modified 2025-08-11 10:24:31