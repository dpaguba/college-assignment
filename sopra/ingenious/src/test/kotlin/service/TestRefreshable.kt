package service

import view.Refreshable

/**
 * This is a Refreshabel dummy. it simulates a gui and the states that were called can be got afterwords.
 * Call [reset] to reset the state vars
 */
class TestRefreshable: Refreshable {

    //Setting up some vars to get the refresh that was called
    var refreshAfterLoadGameCalled: Boolean= false
        private set

    var refreshAfterTurnCalled: Boolean= false
        private set

    var refreshAfterRackSwapableCalled: Boolean= false
        private set

    var refreshAfterBonusRoundCalled: Boolean= false
        private set

    var refreshAfterGameEndCalled: Boolean= false
        private set

    var refreshAfterStartGameCalled: Boolean= false
        private set

    var refreshAfterNetPlayersChangedCalled: Boolean= false
        private set

    var refreshAfterSessionConnectedCalled: Boolean= false
        private set

    var refreshAfterSessionCreatedCalled: Boolean= false
        private set

    /**
     * This reset method will reset the vars that indicate which refreshing service was called
     */
    fun reset() {
        //reset all vars
        refreshAfterLoadGameCalled = false
        refreshAfterTurnCalled = false
        refreshAfterRackSwapableCalled = false
        refreshAfterBonusRoundCalled = false
        refreshAfterGameEndCalled = false
        refreshAfterStartGameCalled = false
        refreshAfterNetPlayersChangedCalled = false
        refreshAfterSessionConnectedCalled = false
        refreshAfterSessionCreatedCalled = false
    }

    override fun refreshAfterLoadGame() {
        refreshAfterLoadGameCalled = true
    }

    override fun refreshAfterTurn() {
        refreshAfterTurnCalled = true
    }

    override fun refreshAfterRackSwappable() {
        refreshAfterRackSwapableCalled = true
    }

    override fun refreshAfterBonusRound() {
        refreshAfterBonusRoundCalled = true
    }

    override fun refreshAfterGameEnd(winner: String) {
        refreshAfterGameEndCalled = true
    }

//    override fun refreshAfterStartGame() {
//        refreshAfterStartGameCalled = true
//    }

    override fun refreshAfterNetPlayersChanged() {
        refreshAfterNetPlayersChangedCalled = true
    }

    override fun refreshAfterSessionConnected() {
        refreshAfterSessionConnectedCalled = true
    }

    override fun refreshAfterSessionCreated() {
        refreshAfterSessionCreatedCalled = true
    }
}