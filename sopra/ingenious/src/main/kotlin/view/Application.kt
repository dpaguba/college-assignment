package view

import entity.Game
import entity.PlayerType
import service.RootService
import tools.aqua.bgw.core.BoardGameApplication


/**
 * The main application class for managing the board game "Ingenious".
 *
 * This class initializes and manages different scenes and game components using the BGW library.
 */
class Application : BoardGameApplication ("Ingenious"),Refreshable {

    /**
     * Central services for all scenes and holds current game as well
     * */
    private var rootService =  RootService()

    /**
     * Initialization of all scenes
     * */
    private var gameScene = GameScene(rootService, this)

    private var gameEndScene = GameEndScene(rootService).apply {
        returnMainMenuBtn.onMouseClicked = {
            this@Application.showMenuScene(mainMenuScene)
        }
    }

    private var loadGameScene = reloadLoadGameScene()

    private var localGameMenuScene = LocalGameMenuScene(rootService)

    private var mainMenuScene = MainMenuScene(rootService).apply {
        loadGameBtn.onMouseClicked = {
            loadGameScene = reloadLoadGameScene()
            this@Application.showMenuScene(loadGameScene)
        }

        newLocalGameBtn.onMouseClicked = {
            this@Application.showMenuScene(localGameMenuScene)
        }

        hostNetworkGameBtn.onMouseClicked = {
            this@Application.showMenuScene(hostNetworkGameScene)
        }

        joinNetworkGameBtn.onMouseClicked = {
            joinNetworkGameScene.joinGamebtn.isDisabled = false
            this@Application.showMenuScene(joinNetworkGameScene)
        }

        exitButton.onMouseClicked = {
            exit()
        }
    }

    private var hostNetworkGameScene = HostNetworkGameScene(rootService)
    private var joinNetworkGameScene = JoinNetworkGameScene(rootService)

    private var pauseScene = PauseScene(rootService).apply {

        cancelBtn.onMouseClicked = {
            hideMenuScene()
            this@Application.showGameScene(gameScene)
        }

        mainMenuBtn.onMouseClicked = {
            this.resetEntities()
            refreshAfterNewGame()
            this@Application.showMenuScene(mainMenuScene)


        }
    }

    private var nextPlayerScene = NextPlayerScene(rootService)

    init {

        /**
         * Register scenes and the application itself as refreshable listeners
         * */
        rootService.addRefreshables(
            this,
            gameScene,
            gameEndScene,
            loadGameScene,
            localGameMenuScene,
            mainMenuScene,
            hostNetworkGameScene,
            joinNetworkGameScene,
            pauseScene,
            nextPlayerScene
        )

        /**
         * Configure callbacks and interactions between scenes
         * */
        gameEndScene.returnMainMenuBtn.onMouseClicked = {
            showMenuScene(mainMenuScene)
            gameEndScene.resetEntiies()
        }

        loadGameScene.cancelBtn.onMouseClicked = {
            showMenuScene(mainMenuScene)
        }

        pauseScene.cancelBtn.onMouseClicked = {
            hideMenuScene()
            showGameScene(gameScene)
        }

        nextPlayerScene.nextPlayerButton.onMouseClicked = {
            rootService.playerService.fillRack()
            hideMenuScene()
            showGameScene(gameScene)

        }

        nextPlayerScene.swapAllButton.onMouseClicked = {
            rootService.playerService.swapRack()
            hideMenuScene()
            showGameScene(gameScene)
        }

        localGameMenuScene.mainMenuBtn.onMouseClicked = {
            showMenuScene(mainMenuScene)
            //delete the current game
            rootService.game = Game(isNetworkGame = false, isTeamMode = false)
            localGameMenuScene.playerList.items.clear()
            localGameMenuScene.addPlayerBtn.isDisabled = false
        }

        hostNetworkGameScene.mainMenuBtn.onMouseClicked={
            showMenuScene(mainMenuScene)
            //delete the current game
            hostNetworkGameScene.resetUi()
        }

        joinNetworkGameScene.mainMenuBtn.onMouseClicked={
            showMenuScene(mainMenuScene)
            //delete the current game
            rootService.game = Game(isNetworkGame = false, isTeamMode = false)
            joinNetworkGameScene.resetUi()
        }

        pauseScene.saveBtn.onMouseClicked = {
            rootService.ioService.storeGame(pauseScene.slotToSave)
            refreshAfterPause()
            pauseScene.resetEntities()
            showMenuScene(mainMenuScene)
        }

        /**
         * Initial scene setup
         * */
        this.showGameScene(gameScene)
        this.showMenuScene(mainMenuScene, 0)

        this.onWindowClosed = { rootService.networkService.disconnect()}
    }

    /**
     * Called when a game is loaded, refreshing the UI.
     */
    override fun refreshAfterLoadGame() {
        this.hideMenuScene()
    }

    /**
     * Called after the game ends, refreshing the UI to show the winner.
     *
     * @param winner The name of the player who won the game.
     */
    override fun refreshAfterGameEnd(winner:String) {
        this.showMenuScene(scene = gameEndScene.apply{
            this.playerWon = winner
        })
    }

    /**
     * Called after each turn, refreshing the UI to show the next player's turn.
     */
    override fun refreshAfterTurn() {
        /*val playerType = rootService.game.currentGameState.
        players[rootService.game.currentGameState.currentPlayerIndex].type
        if(playerType != PlayerType.AI && playerType != PlayerType.AI_RANDOM)
            this.showMenuScene(nextPlayerScene)*/

    }

    /**
     * Called after pressing the pause button
     */

    override fun refreshAfterPause() {
        this.showMenuScene(pauseScene)
    }

    //this is designed only for after clicking the main menu button in the pause scene
    //,that if you want to start a new game the old game (not saved game) will be written over
    //to a new game

    override fun refreshAfterNewGame() {
        this.hideMenuScene()
        rootService = RootService()
        //val gameState = rootService.game.currentGameState
        gameScene = GameScene(rootService, this)
        gameEndScene = GameEndScene(rootService)
        loadGameScene = LoadGameScene(rootService)
        localGameMenuScene = LocalGameMenuScene(rootService)
        mainMenuScene = MainMenuScene(rootService)
        hostNetworkGameScene =HostNetworkGameScene(rootService)
        joinNetworkGameScene = JoinNetworkGameScene(rootService)
        pauseScene =PauseScene(rootService)
        nextPlayerScene =NextPlayerScene(rootService)



        rootService.clear()
        rootService.addRefreshables(
            this,
            gameScene,
            gameEndScene,
            loadGameScene,
            localGameMenuScene,
            mainMenuScene,
            hostNetworkGameScene,
            joinNetworkGameScene,
            pauseScene,
            nextPlayerScene
        )
        this.showGameScene(gameScene)
        this.showMenuScene(mainMenuScene,0)
    }

    override fun refreshAfterRackSwappable() {
        val player = rootService.game.currentGameState.
        players[rootService.game.currentGameState.currentPlayerIndex]
        val playerType = player.type
        if(playerType == PlayerType.LOCAL && player.rackIsSwappable())
            this.showMenuScene(nextPlayerScene)
    }

    private fun reloadLoadGameScene(): LoadGameScene{
        val newScene = LoadGameScene(rootService).apply {
            selectSlot1Btn.onMouseClicked = {
                rootService.ioService.loadGame(0)
                refreshAfterLoadGame()
                hideMenuScene()
            }
            selectSlot2Btn.onMouseClicked = {
                rootService.ioService.loadGame(1)
                refreshAfterLoadGame()
                hideMenuScene()
            }
            selectSlot3Btn.onMouseClicked = {
                rootService.ioService.loadGame(2)
                refreshAfterLoadGame()
                hideMenuScene()
            }
            cancelBtn.onMouseClicked = {
                showMenuScene(mainMenuScene)
            }
        }
        rootService.addRefreshable(newScene)
        return newScene
    }
}

# Modified 2025-08-11 10:24:31