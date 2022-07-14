package entity

import kotlin.collections.mutableListOf

/**
 * Data class DrawStack is characterized by a [CardSuit] and a [CardValue] and stores information
 * about cards on the table
 */
data class Middle(val suit: CardSuit, val value: CardValue) {

    var middle: MutableList<Card> = mutableListOf() // rename into tableCards
}

# Modified 2025-08-11 10:24:33