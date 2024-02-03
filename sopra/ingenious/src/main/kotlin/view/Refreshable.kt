package view

import service.AbstractRefreshingService
import service.ConnectionState


/**
 * This interface provides a mechanism for the service layer classes to communicate
 * (usually to the view classes) that certain changes have been made to the entity
 * layer, so that the user interface can be updated accordingly.
 *
 * Default (empty) implementations are provided for all methods, so that implementing
 * UI classes only need to react to events relevant to them.
 *
 * @see AbstractRefreshingService
 *
 */
interface Refreshable {

    /**
     * Carry out necessary refreshing methods for visual changes in ui layer
     */

    /**
     * refresh after a game is loaded Loadgame/redo/undo
     */
    fun refreshAfterLoadGame() {    }

    /**
     * refresh after the player switches
     *
     * IMPORTANT: CHECK WHAT TYPE OF PLAYER IS PLAYING
     */
    fun refreshAfterTurn(){    }

    /**
     * call that the player can make an action to choose to swap their cards
     */
    fun refreshAfterRackSwappable(){    }

    /**
     * the player can perform another action
     * KI-team this is important for you ;)
     */
    fun refreshAfterBonusRound(){    }

    /**
     * the game hasEnded
     *
     * @param winner winner(team) of this game
     */
    fun refreshAfterGameEnd(winner:String){    }

    /**
     * obsolete since we have afterLoadGame
     * not called from the Services
     */
    fun refreshAfterNewGame(){    }

    /**
     * only important if we are the host.
     * now pull the playerList to show the all players
     * not called from the Services
     */
    fun refreshAfterNetPlayersChanged(){    }

    /**
     * load joinMenuScene
     *
     * most likely obsolete, since we open the joinMenuScene
     * not called from the Services
     */
    fun refreshAfterSessionConnected(){ }

    /**
     * load createMenuScene
     *
     * most likely obsolete, since we open the joinMenuScene
     * not called from the Services
     */
    fun refreshAfterSessionCreated(){   }

    /**
     * close the pauseMenuScene
     *
     * not called from the Services
     */
    fun refreshAfterPause(){    }

    /**
     * calls if the connection State changes, might be important to display Information, if networkPlayers are doing
     * their thing
     * @param connectionState the current connectionState
     */
    fun refreshConnectionState(connectionState: ConnectionState){   }

    /**
     * Refreshes the error-label
     */
    fun refreshError(error: String ){ }

}