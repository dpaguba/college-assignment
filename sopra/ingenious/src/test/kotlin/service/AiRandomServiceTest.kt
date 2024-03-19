package service

import entity.PlayerType
import org.junit.jupiter.api.Test

/**
 * This is the test for the random AI
 */
class AiRandomServiceTest {
    private val rootService = RootService()
    private val playerService = rootService.playerService
    private val gameService = rootService.gameService
    private val aiService = AiRandomService(playerService)

    private fun initGame(){
        gameService.addPlayer("AI", PlayerType.AI_RANDOM)
        gameService.addPlayer("AI", PlayerType.AI_RANDOM)

        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }

    /**
     * Tests make move
     */
    @Test
    fun makeMove() {
        val refreshable = TestRefreshable()

        initGame()
        rootService.addRefreshable(refreshable)

        for(i in 0..20){
            if(refreshable.refreshAfterGameEndCalled)
                break
            aiService.makeMove()
            println("did move $i")
        }

        println(rootService.game.currentGameState.board.fields.toString())
        println(rootService.game.currentGameState.board.fields.size)
    }
}
