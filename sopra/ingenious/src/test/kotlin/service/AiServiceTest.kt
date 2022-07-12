package service

import entity.PlayerType
import org.junit.jupiter.api.Test
import view.Refreshable

/**
 * This is the test for the AI
 */
class AiServiceTest: Refreshable {
    private var rootService = RootService()
    private var gameService = rootService.gameService
    private var playerService = rootService.playerService
    private var aiService = AiService(playerService)
    private var testCount = 0
    private var testsToPerform = 7
    private val winners = arrayListOf<String>()

    private fun initGame(){
        testCount++
        gameService.addPlayer("AI1", PlayerType.AI)
        gameService.addPlayer("AI2r", PlayerType.AI_RANDOM)
        gameService.addPlayer("AI3", PlayerType.AI)
        gameService.addPlayer("AI4r", PlayerType.AI_RANDOM)

        gameService.startGame(isTeamGame = false, isNetworkGame = false)
    }

    /**
     * Tests make move
     */
    @Test
    fun makeMove() {
        val refreshable = TestRefreshable()

        initGame()
        rootService.addRefreshables(refreshable, this)

        // kick the reaction of AI games of:
        aiService.makeMove()




        // aiService.makeMove()
        // var gameState = rootService.game.currentGameState
        /*println("====================================================")
        println("Test $currTest:")
        for (player in rootService.game.currentGameState.players) {
            println("Player ${player.name}: ${player.scoreBoard}")
        }

        println(rootService.game.currentGameState.board.toString())
        println("bag: " + rootService.game.currentGameState.bag.size)
        println("====================================================")
        println()*/
    }

    override fun refreshAfterGameEnd(winner: String) {
        winners.add(winner)
        if (testCount >= testsToPerform){
            println("performed $testCount tests. Winners")
            for ((round,winningPerson) in winners.withIndex()) {
                println("Test $round: Winner: $winningPerson")
            }
            return
        }

        rootService = RootService()
        gameService = rootService.gameService
        playerService = rootService.playerService
        aiService = AiService(playerService)
        makeMove()
    }
}
# Modified 2025-08-11 10:24:32