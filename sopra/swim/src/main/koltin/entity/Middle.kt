package entity

import kotlin.collections.mutableListOf

/**
 * Data class DrawStack is characterized by a [CardSuit] and a [CardValue] and stores information
 * about cards on the table
 * 
 * @property middle contains a list of cards, that are on the table
 */
class Middle() {

    var middle: MutableList<Card> = mutableListOf()
}

# Modified 2025-08-11 10:24:33