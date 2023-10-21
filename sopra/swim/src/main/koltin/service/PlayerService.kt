package service

import entity.*

/**
 * Service layer class that provides the logic for actions not directly related to a single player.
 */
class PlayerService(private val schwimmenService: SchwimmenService) : AbstractRefreshingService() {
    /**
     * Adds new player to the players list of current game
     *
     * Creates Player entity with given name and adds it to the players list
     *
     * @param name name of player
     */
    fun createPlayer(name: String): Player {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        val newPlayer = Player(name)
        game.players.add(newPlayer)
        return newPlayer
    }

    /** Players passes and turn goes to next player */
    fun pass() {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        game.passCounter += 1
        schwimmenService.gameService.checkPassCounter()
        schwimmenService.gameService.finishTurn()
        onAllRefreshables { refreshAfterTurn() }
    }

    /** knock simulates player knocking and end of the game */
    fun knock() {
        val game = schwimmenService.currentGame
        //        checkNotNull(game)
        if (game.players.firstOrNull { it.hasKnocked } == null) {
            game.currentPlayer.hasKnocked = true
        }
        schwimmenService.gameService.finishTurn()
        onAllRefreshables { refreshAfterTurn() }
    }

    /**
     * Swaps one hand card with one table card
     *
     * @param cardOnHand hand card to be swapped
     * @param cardOnMiddle table card that will be swapped to
     */
    fun swapOne(cardOnHand: Card, cardOnMiddle: Card) {
        val game = schwimmenService.currentGame
        val middle = schwimmenService.middle
        //        checkNotNull(game)
        //        checkNotNull(middle)
        game.passCounter = 0
        val indexHand = game.currentPlayer.hand.indexOf(cardOnHand)
        val indexTable = middle.middle.indexOf(cardOnMiddle)
        val tmpCard = cardOnHand
        game.currentPlayer.hand.set(indexHand, cardOnMiddle)
        game.currentPlayer.score = schwimmenService.playerService.getPoints()
        middle.middle.set(indexTable, tmpCard)
        schwimmenService.gameService.finishTurn()
        onAllRefreshables { refreshAfterCardChange() }
        onAllRefreshables { refreshAfterTurn() }
    }

    /** Swaps all hand cards with all table cards */
    fun swapAll() {
        val game = schwimmenService.currentGame
        val middle = schwimmenService.middle
        //        checkNotNull(game)
        //        checkNotNull(middle)
        game.passCounter = 0
        val tmpCards = game.currentPlayer.hand
        game.currentPlayer.hand = mutableListOf()
        game.currentPlayer.hand.addAll(middle.middle)
        game.currentPlayer.score = schwimmenService.playerService.getPoints()
        middle.middle = tmpCards
        schwimmenService.gameService.finishTurn()
        onAllRefreshables { refreshAfterCardChange() }
        onAllRefreshables { refreshAfterTurn() }
    }

    // getPoints returns current player's score
    fun getPoints(): Float {
        return schwimmenService.currentGame.currentPlayer.getPoints()
    }
}
