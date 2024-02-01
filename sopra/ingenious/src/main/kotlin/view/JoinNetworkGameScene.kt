package view

import entity.Game
import entity.PlayerType
import service.ConnectionState
import service.RootService
import tools.aqua.bgw.components.layoutviews.GridPane
import tools.aqua.bgw.components.uicomponents.*
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.visual.ColorVisual

/**
 * Represents the scene where players can join to an already existing networkGame
 *
 * Stolen from HostGameScene
 *
 * @property rootService The [RootService] instance for accessing game-related functionality.
 */
class JoinNetworkGameScene(private val rootService: RootService) : MenuScene(width = 1000, height = 1000,
    background = ColorVisual(
    BACKGROUND_COLOR)
), Refreshable {
    /**
     * The label displaying the title of the local game menu scene.
     */
    private val menuLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Ingenious",
            font = FONT_TITLE
        )

    /**
     * The label displaying the title of the local game menu scene.
     */
    private val playerTypeComboBox : ComboBox<PlayerType> =
        ComboBox(
            width = WIDTH_BUTTON,
            height = HEIGHT_TITLE / 2,
            prompt = "Select player type",
            items = PLAYER_TYPES_LIST
        )

    /**
     * The text field for entering the player name.
     */
    private val playerNameTextField: TextField =
        TextField(
            height = HEIGHT_TITLE / 2,
            width = WIDTH_BUTTON,
            text = "",
            prompt = "Player Name"
        )


    /**
     * Checks if a player type is selected in the combo box.
     */
    private fun isTypeSelected(): Boolean {
        return playerTypeComboBox.selectedItem != null
    }


    /**
     * The button for starting the game with the configured players.
     */
    val joinGamebtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Join Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    ).apply {
        onMouseClicked = {
            if(isTypeSelected()){
                rootService.networkService.joinGame(playerNameTextField.text.trim(),
                    sessionIDInputField.text.trim(),
                    playerTypeComboBox.selectedItem!!)
                this.isDisabled = true }
        }
    }

    val mainMenuBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Main Menu",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )


    /**
     * The label displaying the "Players" title.
     */
//    TO DO change playerList background and add it to grid

    /*private val playersLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Players",
            font = FONT_TITLE
        )*/

    private val sessionIDInputField: TextField =
        TextField(
            height = HEIGHT_TITLE / 2,
            width = WIDTH_BUTTON,
            text = "",
            prompt = "SessionID")

    private val connectionStateLabel: Label = Label(
        height = HEIGHT_TITLE / 2,
        width = WIDTH_BUTTON,
        text = "",
    )
    private val errorLabel: Label = Label(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        //visual = ColorVisual(BACKGROUND_COLOR_BUTTON),
        isWrapText = true
    )
    init {
        addComponents(
            GridPane<UIComponent>(columns = 1, rows = 8, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[0, 1] = playerTypeComboBox
                    this[0, 2] = playerNameTextField
                    this[0, 3] = sessionIDInputField
                    this[0, 4] = joinGamebtn
                    this[0, 5] = connectionStateLabel
                    this[0, 6] = mainMenuBtn
                    this[0, 7] = errorLabel
                    setColumnWidth(0, 1000)
                    setCenterMode(Alignment.CENTER)
                }

        )
        playerTypeComboBox.selectedItem = PLAYER_TYPES_LIST[0]
    }

    /**
     * Refreshes the connectionState
     * @property connectionState The connectionState
     */
    override fun refreshConnectionState(connectionState: ConnectionState) {
        connectionStateLabel.text = connectionState.toString()
    }

    /**
     * Resets the UI, clears all players, activates all inputs
     */
    fun resetUi() {
        rootService.game = Game(isNetworkGame = false, isTeamMode = false)
        rootService.game.currentGameState.players.clear()
        sessionIDInputField.isDisabled = false
        playerNameTextField.isDisabled = false
        playerTypeComboBox.isDisabled = false
        joinGamebtn.isDisabled = false
        rootService.networkService.disconnect()
    }

    /**
     * Refreshes the errorLabel
     */
    override fun refreshError(error: String) {
        errorLabel.text = "Error: $error"
    }

}