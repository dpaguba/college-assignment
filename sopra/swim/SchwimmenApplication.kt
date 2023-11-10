package view

import service.SchwimmenService
import tools.aqua.bgw.core.BoardGameApplication

class SchwimmenApplication : BoardGameApplication("Schwimmen"), Refreshable{

    /**
     * Central service from which all others are created/accessed also holds the currently active game
     */
    private val schwimmenService = SchwimmenService()

    // The actual game takes place here
    private val gameScene = SchwimmenGameScene(schwimmenService).apply {

        // Action for "Swap All" button to swap all hand cards with
        // all table cards
        swapAllButton.onMouseClicked = {
            schwimmenService.playerService.swapAll()
        }

        // Action for "Pass" button to increase pass counter by 1
        passButton.onMouseClicked = {
            schwimmenService.playerService.pass()

        }

        confirmButton.onMouseClicked = {
        }
    }

    // This menu scene is shown after application start
    private val newGameMenuScene = NewGameMenuScene(schwimmenService).apply {
        startButton.onMouseClicked = {
            this@SchwimmenApplication.showGameScene(gameScene)
        }
    }

    private val gameFinishedMenuScene = GameFinishedMenuScene(schwimmenService).apply {
        quitButton.onMouseClicked = {
            exit()
        }

        newGameButton.onMouseClicked = {
            resetGUI()
            this@SchwimmenApplication.showMenuScene(NewGameMenuScene(schwimmenService))
            this@SchwimmenApplication.showGameScene(gameScene)
        }
    }

    init {
        schwimmenService.addRefreshables(
            this,
            gameScene,
            newGameMenuScene,
            gameFinishedMenuScene,
        )

        this.showGameScene(gameScene)
        this.showMenuScene(NewGameMenuScene(schwimmenService), 0)

    }

    override fun refreshAfterStartGame() {
        this@SchwimmenApplication.hideMenuScene()
    }

    override fun refreshAfterGameEnd() {
        this@SchwimmenApplication.showGameScene(gameFinishedMenuScene)
    }


}