package view

import service.SchwimmenService
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.BoardGameScene
import tools.aqua.bgw.util.Font
import tools.aqua.bgw.visual.ColorVisual

class GameFinishedMenuScene(private val schwimmenService: SchwimmenService) : BoardGameScene(1920, 1080), Refreshable{
    private var playerName1st = Label(
        posX = 20, posY = 90,
        width = 400, height = 50,
        text = "",
        font = Font(size = 30),
        alignment = Alignment.CENTER_LEFT
    )
    private var score1st = Label(
        posX = 440, posY = 90,
        width = 300, height = 50,
        text = "",
        font = Font(size = 30)
    )

    private var playername2nd = Label(
        posX = 20, posY = 310,
        width = 400, height = 50,
        text = "",
        font = Font(size = 30),
        alignment = Alignment.CENTER_LEFT
    )
    private var score2nd = Label(
        posX = 440, posY = 310,
        width = 300, height = 50,
        text = "",
        font = Font(size = 30)
    )

    private var playername3rd = Label(
        posX = 20, posY = 530,
        width = 400, height = 50,
        text = "",
        font = Font(size = 30),
        alignment = Alignment.CENTER_LEFT
    ).apply {
        isVisible = false
    }
    private var score3rd = Label(
        posX = 440, posY = 530,
        width = 300, height = 50,
        text = "",
        font = Font(size = 30)
    ).apply {
        isVisible = false
    }

    private var playername4th = Label(
        posX = 20, posY = 750,
        width = 400, height = 50,
        text = "",
        font = Font(size = 30),
        alignment = Alignment.CENTER_LEFT
    ).apply {
        isVisible = false
    }
    private var score4th = Label(
        posX = 440, posY = 750,
        width = 300, height = 50,
        text = "",
        font = Font(size = 30)
    ).apply {
        isVisible = false
    }

    val quitButton = Button(
        width = 200, height = 70,
        posX = 1700, posY = 990,
        text = "Quit",
        font = Font(size = 30)
    ).apply {
        visual = ColorVisual(255, 0, 0)
    }

//    val restartButton = Button(
//        posX = 20, posY = 990,
//        width = 200, height = 70,
//        text = "Restart",
//        font = Font(size = 30)
//    ).apply {
//        visual = ColorVisual(150, 75, 0)
//    }

    val newGameButton = Button(
        posX = 20, posY = 990,
        width = 200, height = 70,
        text = "New Game",
        font = Font(size = 30)
    ).apply {
        visual = ColorVisual(0, 255, 0)
    }

    init {
        background = ColorVisual(108, 168, 59)

        addComponents(
            playerName1st, score1st,
            playername2nd, score2nd,
            playername3rd, score3rd,
            playername4th, score4th,

            newGameButton, quitButton
        )
    }

    /**
     * Function that refreshes scoreboard
     */
    fun refreshGUI() {
        val game = schwimmenService.currentGame
        checkNotNull(game)
        val leaderboard = game.players.sortedWith(compareBy{it.score}).reversed()

        playerName1st.text = "1st: ${leaderboard[0].name}"
        score1st.text = "Score: ${leaderboard[0].score}"
        playername2nd.text = "2nd: ${leaderboard[1].name}"
        score2nd.text = "Score: ${leaderboard[1].score}"

        if (leaderboard.size == 2) return

        for (component in listOf(playername3rd, score3rd)){
            component.isVisible = true
        }

        playername3rd.text = "3rd: ${leaderboard[2].name}"
        score3rd.text = "Score: ${leaderboard[2].score}"

        if (leaderboard.size == 3) return

        for (component in listOf(playername4th, score4th,)){
            component.isVisible = true
        }

        playername4th.text = "4th: ${leaderboard[3].name}"
        score4th.text = "Score: ${leaderboard[3].score}"

    }

    fun resetGUI() {
        for (component in listOf(playername3rd, score3rd)){
            component.isVisible = false
        }
        for (component in listOf(playername4th, score4th)){
            component.isVisible = false
        }
    }

    override fun refreshAfterGameEnd() = refreshGUI()
}

# Modified 2025-08-11 10:24:34