package view

import service.SchwimmenService
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.TextField
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.util.Font
import tools.aqua.bgw.visual.ColorVisual

class NewGameMenuScene(schwimmenService: SchwimmenService) : MenuScene(1920, 1080), Refreshable {

    private val playersFromInput: MutableList<String> = mutableListOf()

    private val player: TextField =
            TextField(
                    width = 300,
                    height = 70,
                    posX = 820,
                    posY = 300,
                    prompt = "Enter player name",
                    font = Font(size = 30)
            )

    val addButton =
            Button(
                            width = 200,
                            height = 70,
                            posX = 750,
                            posY = 505,
                            text = "Add Player",
                            font = Font(size = 30)
                    )
                    .apply {
                        visual = ColorVisual(0, 255, 0)
                        onKeyTyped = { startButton.isDisabled = playersFromInput.size < 2 }
                        onMouseClicked = {
                            playersFromInput.add(player.text.trim())
//                            TODO: add alert, that the player was added to the player list
                            player.text = ""
                        }
                    }

    val startButton =
            Button(
                            width = 200,
                            height = 70,
                            posX = 970,
                            posY = 505,
                            text = "Start game",
                            font = Font(size = 30)
                    )
                    .apply {
                        visual = ColorVisual(0, 255, 0)
                        onMouseClicked = {
                            schwimmenService.gameService.startGame(playersFromInput)
                        }
                    }

    init {
        background = ColorVisual(108, 168, 59)

        addComponents(player, addButton, startButton)
    }
}
