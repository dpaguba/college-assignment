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
 * Represents the scene where players can configure their names and types before starting a local game.
 *
 * Stolen from LocalGameScene
 *
 * @property rootService The [RootService] instance for accessing game-related functionality.
 */
class HostNetworkGameScene(private val rootService: RootService) : MenuScene(
    width = 1200, height = 1000, background = ColorVisual(
        BACKGROUND_COLOR
    )
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
    private val playerTypeComboBox: ComboBox<PlayerType> =
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
    private val startGameBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Start Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    ).apply {
        onMouseClicked = {
            rootService.networkService.startNewHostedGame(gameModeCheckBox.isChecked)
            playerList.items.clear()
        }
    }

    /**
     * The button for starting the game with the configured players.
     */
    private val createGamebtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Create Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    ).apply {
        onMouseClicked = {
            if (isTypeSelected()) {
                rootService.networkService.hostGame(
                    playerNameTextField.text.trim(),
                    sessionIDInputField.text.trim(),
                    playerTypeComboBox.selectedItem!!
                )
                this.isDisabled = true
                sessionIDInputField.isDisabled = true
                playerNameTextField.isDisabled = true
                playerTypeComboBox.isDisabled = true
            }
        }
    }

    private val errorLabel: Label = Label(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        //visual = ColorVisual(BACKGROUND_COLOR_BUTTON),
        isWrapText = true
    )

    /**
     * The button for shuffling the order of players.
     */
    private val shuffleButton: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Shuffle Player Order",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    ).apply {
        onMouseClicked = {
            orderPlayers(playerOrderField.text.split(";"))
        }
    }

    /**
     * Order the Players by a custom order
     *
     * ex: 1;2;3;4 -> 1;2;3;4
     */
    private val playerOrderField: TextField =
        TextField(
            height = HEIGHT_TITLE / 2,
            width = WIDTH_BUTTON,
            text = "",
            prompt = "Custom Order: 1;3;4;2;"
        )

    /**
     * The checkbox to enable or disable the 2v2 game mode.
     */
    private val gameModeCheckBox: CheckBox = CheckBox(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Play a 2v2 Game",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

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
    /*
    private val playersLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Players",
            font = FONT_TITLE
        )*/

    /**
     * The list view displaying the added player names.
     */
    private var playerList: ListView<String> =
        ListView(
            width = WIDTH_BUTTON,
            height = HEIGHT_TITLE * 2,
            items = mutableListOf(),
            font = FONT_PLAYERLIST,
            visual = ColorVisual.BLACK,
            selectionMode = SelectionMode.NONE,
        )

    private val sessionIDInputField: TextField =
        TextField(
            //posY = 900,
            height = HEIGHT_TITLE / 2,
            width = WIDTH_BUTTON,
            text = "",
            prompt = "SessionID"
        )

    private val connectionStateLabel: Label = Label(
        height = HEIGHT_TITLE / 2,
        width = WIDTH_BUTTON,
        text = "",
    )

    private val orderPane = GridPane<UIComponent>(
        posX = 565, posY = 360,
        columns = 1, rows = 2, spacing = 15, layoutFromCenter = false
    ).apply {
        this[0,0] = shuffleButton
        this[0,1] = playerOrderField
        setColumnWidth(0, 600)
        setCenterMode(Alignment.CENTER)
    }


    init {
        addComponents(
            GridPane<UIComponent>(columns = 2, rows = 7, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[1, 1] = playerTypeComboBox
                    this[0, 1] = playerNameTextField
                    this[1, 2] = sessionIDInputField
                    this[0, 3] = playerList
                    this[0, 2] = gameModeCheckBox
                    this[0, 4] = createGamebtn
                    this[0, 5] = errorLabel
                    //this[1, 3] = orderPane
                    this[1, 4] = startGameBtn
                    this[1, 0] = connectionStateLabel
                    this[1, 5] = mainMenuBtn

                    setColumnWidth(0, 600)
                    setCenterMode(Alignment.CENTER)
                },
            orderPane
        )
        playerTypeComboBox.selectedItem = PLAYER_TYPES_LIST[0]
    }

    /**
     * Refreshes after Network players have changed
     */
    override fun refreshAfterNetPlayersChanged() {
        playerList.items.clear()
        for (player in rootService.game.currentGameState.players) {
            val playerString = when (player.type) {
                PlayerType.AI, PlayerType.AI_RANDOM -> {
                    "🤖 ${player.name}"
                }

                PlayerType.LOCAL -> {
                    "👤 ${player.name}"
                }

                else -> {
                    "🖥️ ${player.name}"
                }
            }
            playerList.items.add(playerString)
        }
        errorLabel.text = ""

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
        createGamebtn.isDisabled = false
        playerList.items.clear()
        errorLabel.text = ""
        rootService.networkService.disconnect()
    }

    /**
     * Refreshes the errorLabel
     */
    override fun refreshError(error: String) {
        errorLabel.text = "Error: $error"
    }

    /**
     * makes a given input order to a List in INT for orderPlayers
     */
    private fun orderPlayers(listPos: List<String>) {
        if(listPos.isEmpty()){
            rootService.gameService.shufflePlayers()
            errorLabel.text =""
            return
        }
        var list: List<Int>
        try {
            list = listPos.map { it.toInt() - 1 }
        } catch (e: NumberFormatException) {
            errorLabel.text = "Shuffled Players; FORMAT WAS WRONG: NON INTS DETECTED"
            rootService.gameService.shufflePlayers()
            return
        }
        val gameState = rootService.game.currentGameState
        list = list.distinct()
        if (list.size != gameState.players.size) {
            errorLabel.text = "Shuffled Players; FORMAT WAS WRONG: NON-DISTINCT OR DID NOT MATCH PLAYER COUNT"
            rootService.gameService.shufflePlayers()
            return
        }
        val helperList = mutableListOf<Int>()
        for (i in list.indices) {
            helperList.add(i)
        }
        if (!list.containsAll(helperList)) {
            errorLabel.text = "Shuffled Players: FORMAT WAS WRONG: NOT ALL PLAYER HAVE A POSITION NOW"
            rootService.gameService.shufflePlayers()
            return
        }

        rootService.gameService.orderPlayers(list)
        errorLabel.text =""
    }


}
# Modified 2025-08-11 10:24:32