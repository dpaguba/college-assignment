package entity

import org.junit.jupiter.api.Test

import org.junit.jupiter.api.Assertions.*

class CardTest {

    private val aceClubs = Card(CardSuit.CLUBS, CardValue.ACE)
    private val kingDiamonds = Card(CardSuit.DIAMONDS, CardValue.KING)
    private val queenHearts = Card(CardSuit.HEARTS, CardValue.QUEEN)

    @Test
    fun testToString() {
        kotlin.test.assertEquals("♣" + "A", aceClubs.toString())
        kotlin.test.assertNotEquals("♦" + "J", kingDiamonds.toString())
        kotlin.test.assertEquals("♥" + "Q", queenHearts.toString())
    }
}
