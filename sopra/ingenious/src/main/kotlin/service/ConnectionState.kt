package service

/**
 * A class that contains all current States that are important for the Logic
 * //might be deleted
 */
enum class ConnectionState {
    DISCONNECTED,
    CONNECTED,
    WAIT_FOR_HOST_CONFIRMATION,
    WAIT_FOR_PLAYER_JOIN,
    WAIT_FOR_JOIN_CONFIRMATION,
    WAIT_FOR_GAME_INIT,
    PLAYING_MY_TURN,
    WAITING_FOR_OPPONENT_TURNS
}
# Modified 2025-08-11 10:24:31