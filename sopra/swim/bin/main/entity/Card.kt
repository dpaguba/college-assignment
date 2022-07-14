package entity

/** Data class Card is characterized by a [CardSuit] and a [CardValue] */
data class Card(val suit: CardSuit, val value: CardValue) {

    /** provide two characters to represent card's value. */
    override fun toString() = "$suit$value"
}

# Modified 2025-08-11 10:24:33