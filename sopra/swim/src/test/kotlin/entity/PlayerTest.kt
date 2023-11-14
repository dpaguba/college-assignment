package entity

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

class PlayerTest {

    private var player: Player = Player("Dmytro")

    @Test
    fun testGetPointsAllEqual() {
        player.hand =
                mutableListOf(
                        Card(CardSuit.SPADES, CardValue.ACE),
                        Card(CardSuit.HEARTS, CardValue.ACE),
                        Card(CardSuit.DIAMONDS, CardValue.ACE)
                )
        player.hasKnocked = false
        assertEquals(30.5f, player.getPoints())
    }

    @Test
    fun testGetPointsSumHand() {
        player.hand =
                mutableListOf(
                        Card(CardSuit.SPADES, CardValue.ACE),
                        Card(CardSuit.HEARTS, CardValue.TEN),
                        Card(CardSuit.DIAMONDS, CardValue.SEVEN)
                )
        player.hasKnocked = false
        assertEquals(28.0f, player.getPoints())
    }
}
