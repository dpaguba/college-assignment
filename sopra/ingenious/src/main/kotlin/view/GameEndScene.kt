package view

import entity.Game
import service.RootService
import tools.aqua.bgw.components.layoutviews.GridPane
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.components.uicomponents.LabeledUIComponent
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.visual.ColorVisual

/**
 * Represents the scene displayed at the end of the game.
 *
 * This scene is shown when the game ends and displays the winner's name along with an option to return to the main
 * menu.
 * @property rootService The central service used for managing game state.
 */
class GameEndScene(private val rootService: RootService) : MenuScene(1000,1000,
    ColorVisual(BACKGROUND_COLOR)), Refreshable {

    /**
     * Label indicating the winner of the game.
     *
     * This label displays the name of the player who won the game.
     */
    private val playerWonLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "",
            font = FONT_TITLE
        )

    /**
     * Property representing the winner of the game.
     *
     * This property holds the name of the player who won the game. When set, it also updates the `playerWonLabel`
     * to display a message indicating the winner.
     */
    var playerWon: String = "Player 1"
        set(value) {
            field = value
            playerWonLabel.text = "$value won!"
        }

    /**
     * Button to return to the main menu.
     *
     * This button allows the player to return to the main menu after the game ends.
     */
    val returnMainMenuBtn: Button =
        Button(
            height = HEIGHT_BUTTON,
            width = WIDTH_BUTTON,
            text = "Main Menu",
            font = FONT_BUTTON,
            visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
        )

    init {
        addComponents(
            GridPane<LabeledUIComponent>(columns = 1, rows = 2, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = playerWonLabel
                    this[0, 1] = returnMainMenuBtn

                    setColumnWidth(0, 1000)
                    setCenterMode(Alignment.CENTER)
                }
        )
    }

    /**
     * resets enitites, so that after the game has ended, you can start a new game
     */
    fun resetEntiies() {
        rootService.game = Game(isNetworkGame = false, isTeamMode = false)
    }
}

# Modified 2025-08-11 10:24:31