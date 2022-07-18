package service

import entity.*

/**
 * Service layer class that provides the logic for actions not directly related to a single player.
 */
class GameService(val schwimmenService: SchwimmenService) : AbstractRefreshingService() {
    /** Starts a new game */
    fun startGame(playerNames: MutableList<String>) {
        if (playerNames.size < 2 || playerNames.size > 4) return
        schwimmenService.currentGame = Schwimmen()
        for (name in playerNames) {
            if (name != "") schwimmenService.playerService.createPlayer(name)
        }
        val game = schwimmenService.currentGame
        val middle = schwimmenService.middle
        val drawStack = schwimmenService.drawStack

        game.currentPlayer = game.players[0]

        drawStack.drawStack =
                List(32) { index ->
                            Card(CardSuit.values()[index / 8], CardValue.values()[(index % 8) + 5])
                        }
                        .shuffled()
                        .toMutableList()
        for (player in game.players) {
            player.hand.addAll(
                    drawStack.drawStack.subList(
                            drawStack.drawStack.size - 3,
                            drawStack.drawStack.size
                    )
            )
            player.score = player.getPoints()
            drawStack.drawStack = drawStack.drawStack.subList(0, drawStack.drawStack.size - 3)
        }
        middle.middle.addAll(
                drawStack.drawStack.subList(drawStack.drawStack.size - 3, drawStack.drawStack.size)
        )
        drawStack.drawStack = drawStack.drawStack.subList(0, drawStack.drawStack.size - 3)

        onAllRefreshables { refreshAfterStartGame() }
    }

    /** Checks if it was passed more than 3 times Then resets pass counter. */
    fun checkPassCounter() {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        if (game.passCounter >= game.players.size) {
            renewMiddle()
            game.passCounter = 0
        }
    }

    /** Updates middle with 3 new cards */
    fun renewMiddle() {
        // val game = schwimmenService.currentGame
        val drawStack = schwimmenService.drawStack
        val middle = schwimmenService.middle

        mutableListOf<Card>().also { middle.middle = it }

        if (drawStack.drawStack.size < 3) {
            drawStack.drawStack.shuffle()
        }

        middle.middle.addAll(
                drawStack.drawStack.subList(drawStack.drawStack.size - 3, drawStack.drawStack.size)
        )
        drawStack.drawStack = drawStack.drawStack.subList(0, drawStack.drawStack.size - 3)
    }

    /** Turn goes to next player */
    fun finishTurn() {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        val currentPlayerIndex = game.players.indexOf(game.currentPlayer)
        if (currentPlayerIndex == game.players.lastIndex) game.currentPlayer = game.players[0]
        else game.currentPlayer = game.players[currentPlayerIndex + 1]
        checkKnock()
    }

    /** Checks if any player has knocked. */
    fun checkKnock() {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        if (game.currentPlayer.hasKnocked) endGame()
    }

    /** Ends game */
    fun endGame() {
        onAllRefreshables { refreshAfterGameEnd() }
    }

    /** calculateScore calculates score for each player. */
    fun calculateScore(): List<Pair<String, Float>> {
        val players = schwimmenService.currentGame.players
        val result: List<Pair<String, Float>> = mutableListOf()

        for (player in players) {
            result.apply { (Pair(player.name, player.getPoints())) }
        }

        return result
    }
}

# Modified 2025-08-11 10:24:34