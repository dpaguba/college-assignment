package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

class CardTest {

    private val aceClubs = Card(CardSuit.CLUBS, CardValue.ACE)
    private val kingDiamonds = Card(CardSuit.DIAMONDS, CardValue.KING)
    private val queenHearts = Card(CardSuit.HEARTS, CardValue.QUEEN)

    @Test
    fun testToString() {
        kotlin.test.assertEquals('\u2660' + "A", aceClubs.toString())
        kotlin.test.assertEquals('\u2666' + "J", kingDiamonds.toString())
        kotlin.test.assertEquals('\u2665' + "Q", queenHearts.toString())
    }
}
