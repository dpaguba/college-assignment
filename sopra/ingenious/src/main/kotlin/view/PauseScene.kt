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
import tools.aqua.bgw.visual.ImageVisual

/**
 * Represents the pause menu scene.
 *
 * This scene provides options for the player to save the game or return to the game.
 *
 * @property rootService The central service used for managing game state.
 */
class PauseScene (private val rootService: RootService) : MenuScene(1000,1000,
    ColorVisual(BACKGROUND_COLOR)), Refreshable{

    // An array of saved games with associated images
    private var savedGames : Array<Pair<String, ImageVisual?>> = rootService.ioService.getSavedGames()

    // The selected slot index for saving the game
     var slotToSave = 0

    /**
     * Checks if the specified slot is not empty.
     *
     * @param slot The slot index to check.
     * @return `true` if the slot is not empty, otherwise `false`.
     */
    private fun isNotEmpty(slot: Int) : Boolean{
        return savedGames[slot] != Pair("", null)
    }

    /**
     * Load image path based on the slot's content.
     *
     * @param slot The slot index to load the image for.
     * @return The image path.
     */
    private fun loadImage(slot: Int): String {
        return if (isNotEmpty(slot)){
            "images/saved_game_default.png"
        }else{
            "images/empty_slot.png"
        }
    }



    /**
     * The title label for the Pause scene.
     *
     * This label displays the title "Pause Menu" at the top of the scene.
     */
    private val menuLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Pause Menu",
            font = FONT_TITLE
        )

    /**
     * Buttons for selecting slot for saving game.
     *
     * This button allows the player to select the slot to save the game.
     * It displays an image associated with the slot's content, and it is disabled if the slot is empty.
     */
    private val selectSlot1Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(0))
    ).apply {
        onMouseClicked = {
            slotToSave = 0
        }
    }

    private val selectSlot2Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(1))
    ).apply {
        onMouseClicked = {
            slotToSave = 1
        }
    }

    private val selectSlot3Btn: Button = Button(
        height = HEIGHT_BUTTON * 2,
        width = WIDTH_BUTTON,
        font = FONT_BUTTON,
        visual = ImageVisual(loadImage(2))
    ).apply {
        onMouseClicked = {
            slotToSave = 2
        }
    }

    /**
     * Button for returning to game.
     *
     * This button allows the player to cancel the saving of the game and return to the game.
     */
    val cancelBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Cancel",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for saving to game.
     *
     * This button allows the player to save the game and return to the main menu.
     */
    val saveBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Save",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    /**
     * Button for returning to main menu.
     *
     * This button allows the player to save the game and return to the main menu.
     */
    val mainMenuBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Main Menu",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    init {
        addComponents(
            GridPane<LabeledUIComponent>(columns = 1, rows = 7, spacing = 9, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[0, 1] = selectSlot1Btn
                    this[0, 2] = selectSlot2Btn
                    this[0, 3] = selectSlot3Btn
                    this[0, 4] = saveBtn
                    this[0, 5] = cancelBtn
                    this[0, 6] = mainMenuBtn

                    setColumnWidth(0, 1000)
                    setCenterMode(Alignment.TOP_CENTER)
                }
        )
    }

    /**
     * Resets the entities
     */
    fun resetEntities() {
        rootService.game = Game(isNetworkGame = false, isTeamMode = false)
    }
}

# Modified 2025-08-11 10:24:32