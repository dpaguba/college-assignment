package entity

import java.util.*

/**
 * Enum to distinguish between the 13 possible values in a french-suited card game: 2-10, Jack,
 * Queen, King, and Ace.
 *
 * The values are ordered according to their most common ordering: 2 < 3 < ... < 10 < Jack < Queen <
 * King < Ace
 */
enum class CardValue {
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    TEN,
    JACK,
    QUEEN,
    KING,
    ACE,
    ;

    /**
     * provide a single character to represent this value. Returns one of:
     * 2/3/4/5/6/7/8/9/10/J/Q/K/A
     */
    override fun toString() =
            when (this) {
                TWO -> "2"
                THREE -> "3"
                FOUR -> "4"
                FIVE -> "5"
                SIX -> "6"
                SEVEN -> "7"
                EIGHT -> "8"
                NINE -> "9"
                TEN -> "10"
                JACK -> "J"
                QUEEN -> "Q"
                KING -> "K"
                ACE -> "A"
            }

    fun toInt(): Int {
        when (this) {
            TWO -> return 2
            THREE -> return 3
            FOUR -> return 4
            FIVE -> return 5
            SIX -> return 6
            SEVEN -> return 7
            EIGHT -> return 8
            NINE -> return 9
            TEN -> return 10
            JACK -> return 10
            QUEEN -> return 10
            KING -> return 10
            ACE -> return 11
        }
    }

    companion object {

        /** A set of values for a reduced set of 4x8=32 cards (starting with the 7) */
        fun shortDeck(): Set<CardValue> {
            return EnumSet.of(ACE, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING)
        }
    }
}

# Modified 2025-08-11 10:24:33