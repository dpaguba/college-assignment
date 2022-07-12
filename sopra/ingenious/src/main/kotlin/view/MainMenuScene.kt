package view

import service.RootService
import tools.aqua.bgw.components.layoutviews.GridPane
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.components.uicomponents.LabeledUIComponent
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.visual.ColorVisual


/**
 * Represents the main menu scene of the game.
 *
 * This scene provides options for loading a game, starting a new local game,
 * starting a new network game, and quitting the game.
 *
 * @property rootService The central service used for managing game state.
 */
class MainMenuScene (private val rootService: RootService) : MenuScene(width = 1000, height = 1000,
    background = ColorVisual(
    BACKGROUND_COLOR)), Refreshable{

    /**
     * The main menu label displayed at the top of the main menu scene.
     *
     * This label is used to display the title "Ingenious" at the top of the main menu.
     */
    private val menuLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Ingenious",
            font = FONT_TITLE
        )


    /**
     * Button for loading a saved game.
     *
     * This button allows the player to load a previously saved games.
     */
    val loadGameBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Load Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for starting a new local game.
     *
     * This button enables the player to start a new local game.
     */
    val newLocalGameBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "New Local Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for starting a new network game.
     *
     * This button initiates the creation of a new network game.
     */
    val hostNetworkGameBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Host Network Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for joining network game.
     */
    val joinNetworkGameBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Join Network Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for exiting the game.
     *
     * This button allows the player to exit the game.
     */
    val exitButton: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Quit",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    init {
        addComponents(
            GridPane<LabeledUIComponent>(columns = 1, rows = 6, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[0, 1] = loadGameBtn
                    this[0, 2] = newLocalGameBtn
                    this[0, 3] = hostNetworkGameBtn
                    this[0, 4] = joinNetworkGameBtn
                    this[0, 5] = exitButton

                    setColumnWidth(0, 1000)
                    setCenterMode(Alignment.CENTER)
                })
    }

}

# Modified 2025-08-11 10:24:32