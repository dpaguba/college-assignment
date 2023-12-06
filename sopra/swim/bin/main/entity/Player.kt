package entity

import kotlin.collections.mutableListOf

/**
 * Entity Class represents a player in the game and stores information about player like: player's
 * name, has the player knocked?, hand cards and player's score.
 *
 * @param name
 * - player's name. Can't be empty.
 */
class Player(val name: String) {
    var hasKnocked = false
    var hand = mutableListOf<Card>()
    var score = 0.0

    /** Method getPoints returns player's score */
    fun getPoints(): Double {

        if (checkAllEqual()) {
            score = 30.5
        } else {
            score = sumHand()
        }

        return score
    }

    /** Method checkAllEqual checks whether all cards in the hand are of the same type */
    private fun checkAllEqual(): Boolean {
        var isEqual = true

        for (card in hand) {
            if (card.value != hand[0].value) isEqual = false
        }

        return isEqual
    }

    /** Method sumHand sums card's values and returns the result of type double */
    private fun sumHand(): Double {
        var handCardsValues = hand.toMutableList().map({ it.value.toInt() })

        return handCardsValues.foldRight(0) { total, next -> total + next }.toDouble()
    }
}
