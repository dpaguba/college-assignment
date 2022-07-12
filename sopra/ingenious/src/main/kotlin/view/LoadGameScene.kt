package view

import service.RootService
import tools.aqua.bgw.components.layoutviews.GridPane
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.components.uicomponents.LabeledUIComponent
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.visual.ColorVisual
import tools.aqua.bgw.visual.ImageVisual

/**
 * Represents the scene for loading saved games.
 *
 * This scene allows the player to select a saved game slot to load and continue playing.
 *
 * @property rootService The central service used for managing game state.
 */
class LoadGameScene(private val rootService: RootService) : MenuScene(1000,1000,
    ColorVisual(BACKGROUND_COLOR)), Refreshable {

    // An array of saved games with associated images
    private var savedGames : Array<Pair<String, ImageVisual?>> = rootService.ioService.getSavedGames()

    /**
     * Checks if the specified slot has an associated image.
     *
     * @param slot The slot index to check.
     * @return `true` if the slot has an image, otherwise `false`.
     */
    private fun hasImage(slot : Int) : Boolean {
        return savedGames[slot].second != null
    }

    /**
     * Checks if the specified slot is not empty.
     *
     * @param slot The slot index to check.
     * @return `true` if the slot is not empty, otherwise `false`.
     */
    private fun isNotEmpty(slot: Int) : Boolean{
        return savedGames.isNotEmpty() && savedGames[slot] != Pair("", null)
    }

    /**
     * Load image path based on the slot's content.
     *
     * @param slot The slot index to load the image for.
     * @return The image path.
     */
    private fun loadImage(slot: Int): String {

        return if (isNotEmpty(slot)){
            if (hasImage(slot)){
                "linkToImage"
            }else{
                "images/saved_game_default.png"
            }
        }else{
            "images/empty_slot.png"
        }
    }

    /**
     * The title label for the Load Game scene.
     *
     * This label displays the title "Load Game" at the top of the scene.
     */
    private val menuLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Load Game",
            font = FONT_TITLE
        )

    /**
     * Buttons for selecting saved game slot.
     *
     * This button allows the player to select the saved game slot for loading.
     * It displays an image associated with the slot's content, and it is disabled if the slot is empty.
     */
    val selectSlot1Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(0))
    ).apply {
        if(!isNotEmpty(0)){
            isDisabled = true
        }
    }

    val selectSlot2Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(1))
    ).apply {
        if(!isNotEmpty(1)){
            isDisabled = true
        }
    }

    val selectSlot3Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(2))
    ).apply {
        if(!isNotEmpty(2)){
            isDisabled = true
        }
    }

    /**
     * Button for returning to main menu.
     *
     * This button allows the player to cancel the loading of a saved game and return to the main menu.
     */
    val cancelBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Cancel",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )
    init {
        addComponents(
            GridPane<LabeledUIComponent>(columns = 1, rows = 5, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[0, 1] = selectSlot1Btn
                    this[0, 2] = selectSlot2Btn
                    this[0, 3] = selectSlot3Btn
                    this[0, 4] = cancelBtn

                    setColumnWidth(0, 1000)
                    setCenterMode(Alignment.TOP_CENTER)
                }
        )
    }
}

# Modified 2025-08-11 10:24:32