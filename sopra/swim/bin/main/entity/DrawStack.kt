package entity

/**
 * Data class DrawStack is characterized by a [CardSuit] and a [CardValue] and stores information
 * about cards in draw pile
 */
data class DrawStack(val suit: CardSuit, val value: CardValue) {

    var drawStack: MutableList<Card> = ArrayList(32) // rename into drawPile
}

# Modified 2025-08-11 10:24:33