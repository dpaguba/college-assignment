package service

import entity.Game
import view.Refreshable

/**
 * This is the root service. It must be used to communicate to the other services.
 *
 * @property playerService is an object of the class [PlayerService].
 * @property ioService is an object of the class [IOService].
 * @property gameService is an object of the class [GameService].
 * @property networkService is na object of the class [NetworkService].
 */
class RootService {
    val playerService: PlayerService = PlayerService(this)
    val ioService: IOService = IOService(this)
    val gameService: GameService = GameService(this)
    val networkService: NetworkService = NetworkService(this)
    var game = Game(isNetworkGame = false, isTeamMode = false)
    val aiService = AiService(playerService)
    val aiRandomService = AiRandomService(playerService)
    init {
        addRefreshables(aiService,aiRandomService)
    }

    /**
     * Adds the newRefreshabel to all services
     *
     * @param newRefreshable is the refreshable object to be added
     */
    fun addRefreshable(newRefreshable: Refreshable) {
        playerService.addRefreshable(newRefreshable)
        ioService.addRefreshable(newRefreshable)
        gameService.addRefreshable(newRefreshable)
        networkService.addRefreshable(newRefreshable)
    }

    /**
     * Adds a list of refreshables
     *
     * @param newRefreshables are the refreshables that should be added
     */
    fun addRefreshables(vararg newRefreshables: Refreshable) {
        newRefreshables.forEach { addRefreshable(it) }
    }

    /**
     * Removes the refreshables from the game and player service
     */
    fun clear(){
        gameService.removeRefreshables()
        playerService.removeRefreshables()
    }
}

# Modified 2025-08-11 10:24:31