package view

interface Refreshable {

    /** perform refreshes that are necessary when game ended and end results have to be displayed */
    fun refreshAfterGameEnd() {}

    /** perform refreshes that are necessary after one or all cards were swapped */
    fun refreshAfterCardChange() {}

    /** perform refreshes that are necessary after turn goes to next player */
    fun refreshAfterTurn() {}

    /**
     * perform refreshes that are necessary after player was created and added to the player list
     */
    fun refreshAfterCreatePlayer() {}

    /** perform refreshes after game was started */
    fun refreshAfterStartGame() {}
}

# Modified 2025-08-11 10:24:34