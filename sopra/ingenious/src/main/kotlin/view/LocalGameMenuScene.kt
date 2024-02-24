package view

import entity.PlayerType
import service.RootService
import tools.aqua.bgw.components.layoutviews.GridPane
import tools.aqua.bgw.components.uicomponents.*
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.util.Font
import tools.aqua.bgw.visual.ColorVisual

/**
 * Represents the scene where players can configure their names and types before starting a local game.
 *
 * @property rootService The [RootService] instance for accessing game-related functionality.
 */
class LocalGameMenuScene(private val rootService: RootService) : MenuScene(1200, 1000,
    ColorVisual(BACKGROUND_COLOR)),
    Refreshable {


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
            items = PLAYER_TYPES_LIST,
            font = Font(size = 20)

        ).apply {
            visual = ColorVisual(255, 255, 255)
        }

    /**
     * The text field for entering the player name.
     */
    private val playerNameTextField: TextField =
        TextField(
            height = HEIGHT_TITLE / 2,
            width = WIDTH_BUTTON,
            text = "SoPra",
            prompt = "Player Name",
            font = Font(size = 20)
        )

    /**
     * The button for adding a new player to the game.
     */
    val addPlayerBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Add Player",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    ).apply {
        onMouseClicked = {
            if (playerList.items.size == 3) {
                isDisabled = true
            }
            addNewPLayer()
        }
    }

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
     * Adds a new player with the selected type and entered name to the game.
     */
    private fun addNewPLayer() {

        if (isTypeSelected()) {
            val playerName: String = playerNameTextField.text.trim()
            if (playerName.isNotEmpty()) {
                rootService.gameService.addPlayer(playerName, playerTypeComboBox.selectedItem!!)
            }
        }
        playerNameTextField.text = listOf("Dima", "Clement", "Patrick", "Linus", "Nicolas", "Christian").random()
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
    }


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
            playerList.items.clear()
            rootService.gameService.startGame(isTeamGame = gameModeCheckBox.isChecked, false)
        }
    }

    private val errorLabel: Label = Label(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "",
        isWrapText = true
        //font = FONT_BUTTON,
    )

    /**
     * The label displaying the "Players" title.
     */
//    TO DO: change playerList background and add it to grid
    /*private val playersLabel: Label =
        Label(
            height = HEIGHT_TITLE,
            width = WIDTH_TITLE,
            text = "Players",
            font = FONT_TITLE
        )*/

    /**
     * The list view displaying the added player names.
     */
    var playerList: ListView<String> =
        ListView(
            width = WIDTH_BUTTON,
            height = HEIGHT_TITLE * 2,
            items = mutableListOf(),
            font = FONT_PLAYERLIST,
            visual = ColorVisual.BLACK,
            selectionMode = SelectionMode.NONE,
        )

    /**
     * Button for returning to main menu.
     *
     * This button allows the player to cancel the loading of a saved game and return to the main menu.
     */
    val mainMenuBtn: Button = Button(
        height = HEIGHT_BUTTON,
        width = WIDTH_BUTTON,
        text = "Main Menu",
        font = FONT_BUTTON,
        visual = ColorVisual(BACKGROUND_COLOR_BUTTON)
    )

    private val orderPane = GridPane<UIComponent>(
        posX = 565, posY = 460,
        columns = 1, rows = 2, spacing = 15, layoutFromCenter = false
    ).apply {
        this[0, 0] = shuffleButton
        this[0, 1] = playerOrderField
        setColumnWidth(0, 600)
        setCenterMode(Alignment.CENTER)
    }


    init {
        addComponents(
            GridPane<UIComponent>(columns = 2, rows = 6, spacing = 15, layoutFromCenter = false)
                .apply {
                    this[0, 0] = menuLabel
                    this[0, 1] = playerTypeComboBox
                    this[0, 2] = playerNameTextField
                    this[0, 4] = playerList
                    this[0, 5] = startGameBtn
                    this[1, 0] = errorLabel
                    this[1, 1] = gameModeCheckBox
                    this[1, 2] = addPlayerBtn
                    this[1, 5] = mainMenuBtn

                    setColumnWidth(0, 600)
                    setCenterMode(Alignment.CENTER)
                },
            orderPane
        )
        playerTypeComboBox.selectedItem = PLAYER_TYPES_LIST[0]
    }

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
        //errorLabel.text = ""
    }

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
