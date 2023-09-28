package entity

/**
 * Data class DrawStack is characterized by a [CardSuit] and a [CardValue] and stores information
 * about cards in draw pile
 * 
 * @property drawStack contains all cards, that wasn't used in game so far
 */
class DrawStack() {

    var drawStack: MutableList<Card> = ArrayList(32)
}
