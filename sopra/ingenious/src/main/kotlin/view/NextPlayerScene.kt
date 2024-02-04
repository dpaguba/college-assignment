package view

import service.*
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.core.MenuScene
import tools.aqua.bgw.visual.ColorVisual

/**
 * Extra scene for the transition of current player to next player's turn
 */

class NextPlayerScene(private val rootService: RootService) : MenuScene(1500, 800), Refreshable {
    val nextPlayerButton = Button(
        width = 270, height = 100,
        posX = (width/2)-135, posY = height/2-50,
        text = "Don't swap tiles"
    )

    val swapAllButton = Button(
        width = 270, height = 100,
        posX = (width/2)-135, posY = height/2-200,
        text = "Swap all tiles"
    )


    init {
        background = ColorVisual(0, 0, 0)
        addComponents(
            nextPlayerButton,
            swapAllButton
        )
    }

}