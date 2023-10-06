package entity

import kotlin.collections.mutableListOf

/**
 * Entity Class represents a player in the game and stores information about player like: player's
 * name, has the player knocked?, hand cards and player's score.
 *
 * @param name - player's name. Can't be empty.
 * 
 * @property hasKnocked shows whether the previous player knocked.
 * @property hand is a list of all hand cards.
 * @property score shows player's points.
 */
class Player(val name: String) {
    var hasKnocked = false
    var hand = mutableListOf<Card>()
    var score = 0.0f

    /** Method getPoints returns player's score */
    fun getPoints(): Float {

        if (checkAllEqual()) {
            score = (30.5).toFloat()
        } else {
            score = sumHand()
        }

        return score
    }

    /** Method checkAllEqual checks whether all cards in the hand are of the same type */
    private fun checkAllEqual(): Boolean {
        var isEqual = true

        for (card in hand) {
            if (card.value != hand[0].value){
                isEqual = false
                return isEqual
            }
        }

        return isEqual
    }

    /** Method sumHand sums card's values and returns the result of type double */
    private fun sumHand(): Float {
        var handCardsValues = hand.toMutableList().map({ it.value.toInt() })

        return handCardsValues.foldRight(0) { total, next -> total + next }.toFloat()
    }
}
