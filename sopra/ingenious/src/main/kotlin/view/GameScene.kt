package view

import entity.PlayerType
import entity.TileColor
import entity.TileOrientation
import service.ConnectionState
import service.RootService
import tools.aqua.bgw.components.container.HexagonGrid
import tools.aqua.bgw.components.gamecomponentviews.HexagonView
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.BoardGameScene
import tools.aqua.bgw.event.KeyCode
import tools.aqua.bgw.util.Font
import tools.aqua.bgw.visual.ColorVisual
import tools.aqua.bgw.visual.CompoundVisual
import tools.aqua.bgw.visual.ImageVisual
import tools.aqua.bgw.visual.TextVisual
import java.awt.Color


/**
 * This is the main scene where the game is played in. It contains a board with hexagons as board tile,
 * and the size changes depending on the number of players playing, also on the bottom center lies the current player's
 * score and rack, in the rack will be their own tile pieces. On the (possibly) left right and top part of the scene,
 * other player's statistics will be shown as well, there is also an undo and redo button on the top left side of the
 * scene and a pause game button on the top right.
 * Players have the option to swap a tile or all tile depending on certain circumstances,
 * that will be presented with buttons on the bottom right as well.
 * A text will be shown to indicate the number of bonus rounds acquired for that player during his/her turn
 */
class GameScene(private val rootService: RootService, private val application: Application) :
    BoardGameScene(1920, 1080), Refreshable {
    var game = rootService.game
    private var firstHexSelected = false

    /**
     * Save Indexes for call of service functions
     */
    // Index of the chosen tile from the current players rack
    private var handTileIndex = 0

    // location on which the current player wants to put his tile
    private var boardPos1 = Pair(8, 8)

    /** Undo/Redo/Pause-Buttons:*/
    private val undoButton = Button(
        width = 100, height = 100,
        posX = 100, posY = 100,
        visual = ImageVisual("undo.png")
    ).apply {

        onMouseClicked = {
            if (!rootService.game.isNetworkGame) {
                rootService.gameService.undo()
            }
        }
    }
    private val redoButton = Button(
        width = 100, height = 100,
        posX = 200, posY = 100,
        visual = ImageVisual("redo.png")
    ).apply {

        onMouseClicked = {
            if (!rootService.game.isNetworkGame) {
                try {
                    rootService.gameService.redo()
                } catch (e: Exception) {
                    println(e.toString())
                }
            }
        }
    }
    private val pauseButton = Button(
        width = 75, height = 75,
        posX = 1650, posY = 100,
        visual = ImageVisual("pause.png")
    ).apply {

        onMouseClicked = {
            if (!rootService.game.isNetworkGame) {
                application.refreshAfterPause()
            }
        }
    }

    /** Information Labels for the current player:*/
    private val playerNameLabel = Label(
        width = 400, height = 50,
        posX = 0, posY = 950,
        text = "placeholder", font = Font(size = 50, fontStyle = Font.FontStyle.ITALIC, color = Color.WHITE),
        alignment = Alignment.CENTER
    ).apply {

    }
    private val playerScoreLabel = Label(
        width = 1400, height = 35,
        posX = 500, posY = 1040,
        text = "Score:",
        font = Font(size = 26, color = Color.WHITE)
    ).apply {

    }
    private val bonusRoundLabel = Label(
        width = 500, height = 35,
        posX = 650, posY = 800,
        text = "You have a bonus round left ",
        font = Font(size = 26,color = Color.WHITE)
    ).apply {
        visual = ColorVisual.GRAY
        isVisible = false
    }


    /** NextAI move Tile Button: */
    private val nextAIMoveButton = Button(
        width = 200, height = 35,
        posX = 1620, posY = 1000,
        text = "Next AI move", font = Font(size = 26, color = Color.WHITE)
    ).apply {
        visual= ColorVisual.GRAY
        onMouseClicked = {
            rootService.gameService.startAI()
        }
        isVisible = false
        isDisabled = false
    }

    /** Tiles of the current player*/
    private val handTile1 = HexagonView(
        posX = 500, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 0
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile2 = HexagonView(
        posX = 570, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 0
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile3 = HexagonView(
        posX = 670, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 1
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile4 = HexagonView(
        posX = 740, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 1
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile5 = HexagonView(
        posX = 840, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 2
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile6 = HexagonView(
        posX = 910, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 2
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile7 = HexagonView(
        posX = 1010, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 3
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile8 = HexagonView(
        posX = 1080, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 3
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile9 = HexagonView(
        posX = 1180, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 4
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile10 = HexagonView(
        posX = 1250, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 4
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile11 = HexagonView(
        posX = 1350, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 5
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }
    private val handTile12 = HexagonView(
        posX = 1420, posY = 900, size = 40,
        visual = ColorVisual.TRANSPARENT
    ).apply {
        onMouseClicked = {
            handTileIndex = 5
            //handTileLabel.text = handTileIndex.toString()
            liftTiles()
        }
    }


    private val xOffsetPlayerNRack = 30
    private var currOffset = 0
    private val player0Rack = Array(12, init = {
        HexagonView(
            posX = 10 + currOffset, posY = 300, size = 20,
            visual = ColorVisual.TRANSPARENT
        ).apply {
            currOffset += xOffsetPlayerNRack
            if (it % 2 == 1)
                currOffset += 20
            if (it == 11)
                currOffset = 0
        }
    })
    private val player1Rack = Array(12, init = {
        HexagonView(
            posX = 10 + currOffset, posY = 500, size = 20,
            visual = ColorVisual.TRANSPARENT
        ).apply {
            currOffset += xOffsetPlayerNRack
            if (it % 2 == 1)
                currOffset += 20
            if (it == 11)
                currOffset = 0
        }
    })
    private val player2Rack = Array(12, init = {
        HexagonView(
            posX = 1430 + currOffset, posY = 300, size = 20,
            visual = ColorVisual.TRANSPARENT
        ).apply {
            currOffset += xOffsetPlayerNRack
            if (it % 2 == 1)
                currOffset += 20
            if (it == 11)
                currOffset = 0
        }
    })
    private val player3Rack = Array(12, init = {
        HexagonView(
            posX = 1430 + currOffset, posY = 500, size = 20,
            visual = ColorVisual.TRANSPARENT
        ).apply {
            currOffset += xOffsetPlayerNRack
            if (it % 2 == 1)
                currOffset += 20
            if (it == 11)
                currOffset = 0
        }
    })

    private val player0label = Label(
        width = 200, height = 35,
        posX = 10, posY = 250,
        text = "Player 0", font = Font(size = 26, color = Color.WHITE)
    ).apply {

        isVisible = false
    }

    private val player1label = Label(
        width = 200, height = 35,
        posX = 10, posY = 450,
        text = "Player 1", font = Font(size = 26, color = Color.WHITE)
    ).apply {
        isVisible = false
    }
    private val player2label = Label(
        width = 200, height = 35,
        posX = 1620, posY = 250,
        text = "Player 2", font = Font(size = 26, color = Color.WHITE)
    ).apply {
        isVisible = false
    }
    private val player3label = Label(
        width = 200, height = 35,
        posX = 1620, posY = 450,
        text = "Player 3", font = Font(size = 26, color = Color.WHITE)
    ).apply {
        isVisible = false
    }


    private val redScore = Label(
        width = 90, height = 50,
        posX = 750, posY = 1020,
        //visual = CompoundVisual(ColorVisual.RED, TextVisual("0"))
    )
    private val greenScore = Label(
        width = 90, height = 50,
        posX = 840, posY = 1020,
        //visual = CompoundVisual(ColorVisual.GREEN, TextVisual("0"))
    )
    private val blueScore = Label(
        width = 90, height = 50,
        posX = 930, posY = 1020,
        //visual = CompoundVisual(ColorVisual.BLUE, TextVisual("0"))
    )
    private val orangeScore = Label(
        width = 90, height = 50,
        posX = 1020, posY = 1020,
        //visual = CompoundVisual(ColorVisual.ORANGE, TextVisual("0"))
    )
    private val yellowScore = Label(
        width = 90, height = 50,
        posX = 1110, posY = 1020,
        //visual = CompoundVisual(ColorVisual.YELLOW, TextVisual("0"))
    )
    private val purpleScore = Label(
        width = 90, height = 50,
        posX = 1200, posY = 1020,
        //visual = CompoundVisual(ColorVisual.MAGENTA, TextVisual("0"))
    )

    private val p0redScore = Label(
        width = 50, height = 50,
        posX = 10, posY = 370,
    )

    private val p0greenScore = Label(
        width = 50, height = 50,
        posX = 60, posY = 370,

        )
    private val p0blueScore = Label(
        width = 50, height = 50,
        posX = 110, posY = 370,
    )
    private val p0orangeScore = Label(
        width = 50, height = 50,
        posX = 160, posY = 370,
    )
    private val p0yellowScore = Label(
        width = 50, height = 50,
        posX = 210, posY = 370,
    )
    private val p0purpleScore = Label(
        width = 50, height = 50,
        posX = 260, posY = 370,
    )

    private val p1redScore = Label(
        width = 50, height = 50,
        posX = 10, posY = 570,
    )

    private val p1greenScore = Label(
        width = 50, height = 50,
        posX = 60, posY = 570,

        )
    private val p1blueScore = Label(
        width = 50, height = 50,
        posX = 110, posY = 570,
    )
    private val p1orangeScore = Label(
        width = 50, height = 50,
        posX = 160, posY = 570,
    )
    private val p1yellowScore = Label(
        width = 50, height = 50,
        posX = 210, posY = 570,
    )
    private val p1purpleScore = Label(
        width = 50, height = 50,
        posX = 260, posY = 570,
    )

    private val p2redScore = Label(
        width = 50, height = 50,
        posX = 1520, posY = 370,
    )

    private val p2greenScore = Label(
        width = 50, height = 50,
        posX = 1570, posY = 370,

        )
    private val p2blueScore = Label(
        width = 50, height = 50,
        posX = 1620, posY = 370,
    )
    private val p2orangeScore = Label(
        width = 50, height = 50,
        posX = 1670, posY = 370,
    )
    private val p2yellowScore = Label(
        width = 50, height = 50,
        posX = 1720, posY = 370,
    )
    private val p2purpleScore = Label(
        width = 50, height = 50,
        posX = 1770, posY = 370,
    )

    private val p3redScore = Label(
        width = 50, height = 50,
        posX = 1520, posY = 570,
    )

    private val p3greenScore = Label(
        width = 50, height = 50,
        posX = 1570, posY = 570,

        )
    private val p3blueScore = Label(
        width = 50, height = 50,
        posX = 1620, posY = 570,
    )
    private val p3orangeScore = Label(
        width = 50, height = 50,
        posX = 1670, posY = 570,
    )
    private val p3yellowScore = Label(
        width = 50, height = 50,
        posX = 1720, posY = 570,
    )
    private val p3purpleScore = Label(
        width = 50, height = 50,
        posX = 1770, posY = 570,
    )
    private var hexagonGrid: HexagonGrid<HexagonView> = HexagonGrid(
        coordinateSystem = HexagonGrid.CoordinateSystem.AXIAL,
        posX = 910.0, posY = 380
    )

    init {
        background = ImageVisual("mario_background.jpg")

        // Add necessary components
        addComponents(
            playerNameLabel,/*playerScoreLabel, bonusRoundLabel, handTileLabel, boardPos1Label,*/
            undoButton, redoButton, pauseButton, nextAIMoveButton,
            hexagonGrid,
            handTile1, handTile2, handTile3, handTile4, handTile5,
            handTile6, handTile7, handTile8, handTile9, handTile10, handTile11, handTile12,
            redScore, greenScore, blueScore, orangeScore, yellowScore, purpleScore,
            player0label, player1label, player2label, player3label,
            p0redScore, p0greenScore, p0blueScore, p0orangeScore, p0purpleScore, p0yellowScore,
            p1redScore, p1greenScore, p1blueScore, p1orangeScore, p1purpleScore, p1yellowScore,
            p2redScore, p2greenScore, p2blueScore, p2orangeScore, p2purpleScore, p2yellowScore,
            p3redScore, p3greenScore, p3blueScore, p3orangeScore, p3purpleScore, p3yellowScore,
            bonusRoundLabel
        )


        // Add Other player's components
        for (hex in player0Rack) {
            addComponents(hex)
        }
        for (hex in player1Rack) {
            addComponents(hex)
        }
        for (hex in player2Rack) {
            addComponents(hex)
        }
        for (hex in player3Rack) {
            addComponents(hex)
        }
    }

    private fun initBoard() {
        game = rootService.game
        val gameState = game.currentGameState
        gameState.players[gameState.currentPlayerIndex]
        for (column in gameState.board.getRowRange(0).first..gameState.board.getRowRange(0).second) {
            for (row in gameState.board.getColumnRange(column).first..
                    gameState.board.getColumnRange(column).second) {
                val hexagon = HexagonView(
                    //visual = CompoundVisual(ColorVisual.LIGHT_GRAY, TextVisual("($column, $row)"))
                    visual = ColorVisual.LIGHT_GRAY, size = 35
                )
                hexagonGrid[row, column] = hexagon
                hexagon.onMouseClicked = {
                    val currGameStat = rootService.game.currentGameState
                    val currPlayer = currGameStat.players[currGameStat.currentPlayerIndex]
                    if (currPlayer.type == PlayerType.LOCAL
                        && currGameStat.board.getTileColor(column, row) == TileColor.EMPTY
                        && testFirstRoundValidity(column, row)
                    ) {
                        this.onKeyPressed = { event ->
                            if (event.keyCode == KeyCode.ESCAPE) {
                                if (firstHexSelected)
                                    hexagon.visual = ColorVisual.GRAY
                                firstHexSelected = false
                            }
                        }
                        println("Hexagon clicked: $row, $column")
                        if (!firstHexSelected) {
                            boardPos1 = Pair(column, row)
                            //boardPos1Label.text = "Pos 1st color:$boardPos1"
                            /*val currGameStat = rootService.game.currentGameState
                            val currPlayer = currGameStat.players[currGameStat.currentPlayerIndex]*/
                            if (handTileIndex < currPlayer.rack.size) {
                                val tileOnRack = currPlayer.rack[handTileIndex]
                                hexagon.visual = CompoundVisual(colorToVisual(tileOnRack.firstColor),
                                    TextVisual("⤵"))
                                firstHexSelected = true
                            }
                        } else {
                            // next click is direction
                            val direction = when {
                                (boardPos1.first == column && boardPos1.second > row) ->
                                    TileOrientation.LEFT

                                (boardPos1.first > column && boardPos1.second == row) ->
                                    TileOrientation.UP_LEFT

                                (boardPos1.first > column && boardPos1.second < row) ->
                                    TileOrientation.UP_RIGHT

                                (boardPos1.first == column && boardPos1.second < row) ->
                                    TileOrientation.RIGHT

                                (boardPos1.first < column && boardPos1.second == row) ->
                                    TileOrientation.DOWN_RIGHT

                                (boardPos1.first < column && boardPos1.second > row) ->
                                    TileOrientation.DOWN_LEFT

                                else -> null
                            }
                            if (direction != null) {
                                firstHexSelected = false
                                //hexagon.visual = CompoundVisual(ColorVisual.GRAY, TextVisual("($column, $row)"))
                                hexagon.visual = ColorVisual.GRAY
                                placeTile(direction)
                            }
                        }
                    } else {
                        if (currPlayer.type == PlayerType.AI || currPlayer.type == PlayerType.AI_RANDOM) {
                            // If it's the AI's turn and the board has been clicked: Make next AI move
                            rootService.gameService.startAI()
                        }
                    }
                }
            }
        }

        // Lift the selected tile
        liftTiles()
    }

    /**
     * Returns true if the selected position makes sense in the first round
     */
    private fun testFirstRoundValidity(column: Int, row: Int): Boolean {
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]
        if (!player.isInFirstRound)
            return true
        // quick botch to get this working
        val validPositions = arrayListOf<Pair<Int, Int>>()
        // go through every start:
        val board = gameState.board
        val starts = arrayListOf(Pair(-5, 0), Pair(-5, 5), Pair(0, 5), Pair(5, 0), Pair(5, -5), Pair(0, -5))

        val freeStarts = arrayListOf<Pair<Int, Int>>()

        for (start in starts) {
            if (!rootService.playerService.hasANeighbour(start.first, start.second)) {
                freeStarts.add(start)
            }
        }

        for (start in freeStarts) {
            // go the first field connected to the start field
            for (firstDir in TileOrientation.values()) {
                val firstOff = firstDir.orientationToCoordinatePair()
                if (board.isInGameBoard(start.first + firstOff.first, start.second + firstOff.second)) {
                    // Go to the second field, which is in the game board
                    for (secondDir in TileOrientation.values()) {
                        if (secondDir != rootService.playerService.getReversedLine(firstDir)) {
                            val secondOff = secondDir.orientationToCoordinatePair()
                            if (board.isInGameBoard(
                                    start.first + firstOff.first + secondOff.first,
                                    start.second + firstOff.second + secondOff.second
                                )
                            ) {
                                validPositions.add(Pair(start.first + firstOff.first, start.second + firstOff.second))
                                validPositions.add(
                                    Pair(
                                        start.first + firstOff.first + secondOff.first,
                                        start.second + firstOff.second + secondOff.second
                                    )
                                )
                            }
                        }
                    }
                }
            }
        }

        // if in middle:
        return (validPositions.contains(Pair(column, row)))
    }

    private fun updatePlayer() {
        val gameState = game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]

        playerScoreLabel.text = "Your score: ${player.scoreBoard}"
        playerNameLabel.text = player.name + "'s Turn"


    }

    private fun updateRack() {
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]
        val rack = player.rack
        /*if (player.rackIsSwappable()){
            swapAllTileButton.isDisabled = false
            swapAllTileButton.isVisible = true
        }*/

        // make all tiles transparent
        handTile1.visual = ColorVisual.TRANSPARENT
        handTile2.visual = ColorVisual.TRANSPARENT
        handTile4.visual = ColorVisual.TRANSPARENT
        handTile5.visual = ColorVisual.TRANSPARENT
        handTile6.visual = ColorVisual.TRANSPARENT
        handTile7.visual = ColorVisual.TRANSPARENT
        handTile8.visual = ColorVisual.TRANSPARENT
        handTile9.visual = ColorVisual.TRANSPARENT
        handTile10.visual = ColorVisual.TRANSPARENT
        handTile11.visual = ColorVisual.TRANSPARENT
        handTile12.visual = ColorVisual.TRANSPARENT

        // set them
        handTile1.visual = colorToVisual(rack[0].firstColor)
        handTile2.visual = colorToVisual(rack[0].secondColor)
        if (rack.size <= 1)
            return
        handTile3.visual = colorToVisual(rack[1].firstColor)
        handTile4.visual = colorToVisual(rack[1].secondColor)
        if (rack.size <= 2)
            return
        handTile5.visual = colorToVisual(rack[2].firstColor)
        handTile6.visual = colorToVisual(rack[2].secondColor)
        if (rack.size <= 3)
            return
        handTile7.visual = colorToVisual(rack[3].firstColor)
        handTile8.visual = colorToVisual(rack[3].secondColor)
        if (rack.size <= 4)
            return
        handTile9.visual = colorToVisual(rack[4].firstColor)
        handTile10.visual = colorToVisual(rack[4].secondColor)
        if (rack.size <= 5)
            return
        handTile11.visual = colorToVisual(rack[5].firstColor)
        handTile12.visual = colorToVisual(rack[5].secondColor)
    }


    private fun updateBoard() {
        val gameState = rootService.game.currentGameState
        val board = gameState.board

        var column = gameState.board.getRowRange(0).first
        while (column <= gameState.board.getRowRange(0).second) {
            for (row in gameState.board.getColumnRange(column).first..
                    gameState.board.getColumnRange(column).second) {
                val boardType = board.getTileColor(column, row)

                //val color = colorToVisual(boardType)

                //hexagonGrid[row, column]!!.visual = CompoundVisual(color, TextVisual("($column, $row)"))
                hexagonGrid[row, column]!!.visual = colorToVisual(boardType)
            }
            column++
        }
        updateOtherPlayerRacks()
        updateOtherPlayersScore()
    }


    private fun resetUI() {
        undoButton.isDisabled = false
        redoButton.isDisabled = false
        /*swapAllTileButton.isDisabled = true
        swapAllTileButton.isVisible = false*/
    }

    private fun updateScore() {
        val scoreboard = rootService.game.currentGameState.players[game.currentGameState.currentPlayerIndex].scoreBoard
        redScore.visual =
            CompoundVisual(ColorVisual.RED, TextVisual(scoreboard[TileColor.RED].toString(), font = Font(size = 35)))
        greenScore.visual = CompoundVisual(
            ColorVisual.GREEN,
            TextVisual(scoreboard[TileColor.GREEN].toString(), font = Font(size = 35))
        )
        blueScore.visual =
            CompoundVisual(ColorVisual.BLUE, TextVisual(scoreboard[TileColor.BLUE].toString(), font = Font(size = 35)))
        orangeScore.visual = CompoundVisual(
            ColorVisual.ORANGE,
            TextVisual(scoreboard[TileColor.ORANGE].toString(), font = Font(size = 35))
        )
        yellowScore.visual = CompoundVisual(
            ColorVisual.YELLOW,
            TextVisual(scoreboard[TileColor.YELLOW].toString(), font = Font(size = 35))
        )
        purpleScore.visual = CompoundVisual(
            ColorVisual.MAGENTA,
            TextVisual(scoreboard[TileColor.PURPLE].toString(), font = Font(size = 35))
        )
    }


    // This method creates a new game ,as well as loads existing game
    override fun refreshAfterLoadGame() {
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]

        initBoard()
        updateRack()
        updateBoard()
        updateScore()


        //playerScoreLabel.text = "Your score:${player.scoreBoard}"
        playerNameLabel.text = player.name + "'s Turn"
        nextAIMoveButton.isVisible = (player.type == PlayerType.AI || player.type == PlayerType.AI_RANDOM)
    }

    override fun refreshAfterTurn() {
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]
        updateRack()
        updateBoard()
        updatePlayer()
        resetUI()
        updateScore()


        // playerScoreLabel.text = "Your score: ${player.scoreBoard}"
        playerNameLabel.text = player.name + "'s Turn"
        // hide the bonus round lable
        bonusRoundLabel.isVisible = false
        nextAIMoveButton.isVisible = (player.type == PlayerType.AI || player.type == PlayerType.AI_RANDOM)
    }

    override fun refreshAfterBonusRound() {
        val gameState = rootService.game.currentGameState
        val player = gameState.players[gameState.currentPlayerIndex]
        updateRack()
        updateBoard()
        updatePlayer()
        resetUI()
        updateScore()

        // show the bonus round lable
        bonusRoundLabel.isVisible = true

        // playerScoreLabel.text = "Your score: ${player.scoreBoard}"
        playerNameLabel.text = player.name + "'s Turn"
        nextAIMoveButton.isVisible = (player.type == PlayerType.AI || player.type == PlayerType.AI_RANDOM)
    }

    /**
     * Help method which converts a TileColor to a ColorVisual
     */
    private fun colorToVisual(color: TileColor): ColorVisual {
        return when (color) {
            TileColor.PURPLE -> ColorVisual.MAGENTA
            TileColor.RED -> ColorVisual.RED
            TileColor.GREEN -> ColorVisual.GREEN
            TileColor.BLUE -> ColorVisual.BLUE
            TileColor.YELLOW -> ColorVisual.YELLOW
            TileColor.ORANGE -> ColorVisual.ORANGE
            TileColor.EMPTY -> ColorVisual.GRAY
            TileColor.OUT_OF_BOARD -> ColorVisual.TRANSPARENT
        }
    }

    private fun placeTile(orient: TileOrientation) {
        val board = game.currentGameState.board
        val posFstCol = boardPos1

        val off = orient.orientationToCoordinatePair()
        if (board.isInGameBoard(posFstCol.first, posFstCol.second) &&
            board.isInGameBoard(posFstCol.first + off.first, posFstCol.second + off.second)
        ) {
            if (board.getTileColor(posFstCol.first, posFstCol.second) == TileColor.EMPTY &&
                board.getTileColor(
                    posFstCol.first + off.first,
                    posFstCol.second + off.second
                ) == TileColor.EMPTY
            ) {
                if (game.currentGameState.players[game.currentGameState.currentPlayerIndex].isInFirstRound) {
                    if (rootService.playerService.isPlacedToNewStartSymbol(
                            posFstCol.first, posFstCol.second,
                            orient
                        )
                    ) {
                        rootService.playerService.placeTile(
                            handTileIndex, posFstCol.first, posFstCol.second,
                            orient
                        )
                    }
                } else {
                    rootService.playerService.placeTile(
                        handTileIndex, posFstCol.first, posFstCol.second,
                        orient
                    )
                }
            }
        }
    }

    private fun liftTiles() {
        val defaultVal = 900.0
        val liftedVal = 880.0
        //reset all Tiles
        handTile1.posY = defaultVal
        handTile2.posY = defaultVal
        handTile3.posY = defaultVal
        handTile4.posY = defaultVal
        handTile5.posY = defaultVal
        handTile6.posY = defaultVal
        handTile7.posY = defaultVal
        handTile8.posY = defaultVal
        handTile9.posY = defaultVal
        handTile10.posY = defaultVal
        handTile11.posY = defaultVal
        handTile12.posY = defaultVal
        // set only the selected one
        when (handTileIndex) {
            0 -> {
                handTile1.posY = liftedVal
                handTile2.posY = liftedVal
            }

            1 -> {
                handTile3.posY = liftedVal
                handTile4.posY = liftedVal
            }

            2 -> {
                handTile5.posY = liftedVal
                handTile6.posY = liftedVal
            }

            3 -> {
                handTile7.posY = liftedVal
                handTile8.posY = liftedVal
            }

            4 -> {
                handTile9.posY = liftedVal
                handTile10.posY = liftedVal
            }

            5 -> {
                handTile11.posY = liftedVal
                handTile12.posY = liftedVal
            }
        }
    }

    private fun updateOtherPlayersScore() {

        val gameState = rootService.game.currentGameState
        val playerCount = gameState.players.size
        val p0scoreboard = gameState.players[0].scoreBoard
        val p1scoreboard = gameState.players[1].scoreBoard



        p0redScore.visual = CompoundVisual(ColorVisual.RED, TextVisual(p0scoreboard[TileColor.RED].toString()))
        p0greenScore.visual = CompoundVisual(ColorVisual.GREEN, TextVisual(p0scoreboard[TileColor.GREEN].toString()))
        p0blueScore.visual = CompoundVisual(ColorVisual.BLUE, TextVisual(p0scoreboard[TileColor.BLUE].toString()))
        p0orangeScore.visual = CompoundVisual(ColorVisual.ORANGE, TextVisual(p0scoreboard[TileColor.ORANGE].toString()))
        p0yellowScore.visual = CompoundVisual(ColorVisual.YELLOW, TextVisual(p0scoreboard[TileColor.YELLOW].toString()))
        p0purpleScore.visual =
            CompoundVisual(ColorVisual.MAGENTA, TextVisual(p0scoreboard[TileColor.PURPLE].toString()))

        p1redScore.visual = CompoundVisual(ColorVisual.RED, TextVisual(p1scoreboard[TileColor.RED].toString()))
        p1greenScore.visual = CompoundVisual(ColorVisual.GREEN, TextVisual(p1scoreboard[TileColor.GREEN].toString()))
        p1blueScore.visual = CompoundVisual(ColorVisual.BLUE, TextVisual(p1scoreboard[TileColor.BLUE].toString()))
        p1orangeScore.visual = CompoundVisual(ColorVisual.ORANGE, TextVisual(p1scoreboard[TileColor.ORANGE].toString()))
        p1yellowScore.visual = CompoundVisual(ColorVisual.YELLOW, TextVisual(p1scoreboard[TileColor.YELLOW].toString()))
        p1purpleScore.visual =
            CompoundVisual(ColorVisual.MAGENTA, TextVisual(p1scoreboard[TileColor.PURPLE].toString()))

        if (playerCount == 3) {
            val p2scoreboard = gameState.players[2].scoreBoard
            p2redScore.visual = CompoundVisual(ColorVisual.RED, TextVisual(p2scoreboard[TileColor.RED].toString()))
            p2greenScore.visual =
                CompoundVisual(ColorVisual.GREEN, TextVisual(p2scoreboard[TileColor.GREEN].toString()))
            p2blueScore.visual = CompoundVisual(ColorVisual.BLUE, TextVisual(p2scoreboard[TileColor.BLUE].toString()))
            p2orangeScore.visual =
                CompoundVisual(ColorVisual.ORANGE, TextVisual(p2scoreboard[TileColor.ORANGE].toString()))
            p2yellowScore.visual =
                CompoundVisual(ColorVisual.YELLOW, TextVisual(p2scoreboard[TileColor.YELLOW].toString()))
            p2purpleScore.visual =
                CompoundVisual(ColorVisual.MAGENTA, TextVisual(p2scoreboard[TileColor.PURPLE].toString()))
        }

        if (playerCount == 4) {
            val p2scoreboard = gameState.players[2].scoreBoard
            p2redScore.visual = CompoundVisual(ColorVisual.RED, TextVisual(p2scoreboard[TileColor.RED].toString()))
            p2greenScore.visual =
                CompoundVisual(ColorVisual.GREEN, TextVisual(p2scoreboard[TileColor.GREEN].toString()))
            p2blueScore.visual = CompoundVisual(ColorVisual.BLUE, TextVisual(p2scoreboard[TileColor.BLUE].toString()))
            p2orangeScore.visual =
                CompoundVisual(ColorVisual.ORANGE, TextVisual(p2scoreboard[TileColor.ORANGE].toString()))
            p2yellowScore.visual =
                CompoundVisual(ColorVisual.YELLOW, TextVisual(p2scoreboard[TileColor.YELLOW].toString()))
            p2purpleScore.visual =
                CompoundVisual(ColorVisual.MAGENTA, TextVisual(p2scoreboard[TileColor.PURPLE].toString()))

            val p3scoreboard = gameState.players[3].scoreBoard
            p3redScore.visual = CompoundVisual(ColorVisual.RED, TextVisual(p3scoreboard[TileColor.RED].toString()))
            p3greenScore.visual =
                CompoundVisual(ColorVisual.GREEN, TextVisual(p3scoreboard[TileColor.GREEN].toString()))
            p3blueScore.visual = CompoundVisual(ColorVisual.BLUE, TextVisual(p3scoreboard[TileColor.BLUE].toString()))
            p3orangeScore.visual =
                CompoundVisual(ColorVisual.ORANGE, TextVisual(p3scoreboard[TileColor.ORANGE].toString()))
            p3yellowScore.visual =
                CompoundVisual(ColorVisual.YELLOW, TextVisual(p3scoreboard[TileColor.YELLOW].toString()))
            p3purpleScore.visual =
                CompoundVisual(ColorVisual.MAGENTA, TextVisual(p3scoreboard[TileColor.PURPLE].toString()))
        }
    }

    private fun updateOtherPlayerRacks() {
        val gameState = rootService.game.currentGameState
        val playerCount = gameState.players.size
        // For player 0
        val player0RackUpdated = gameState.players[0].rack

        player0label.text = gameState.players[0].name + "'s Stats"
        player0label.isVisible = true

        for (visTile in player0Rack) {
            visTile.visual = ColorVisual.TRANSPARENT

        }
        var j = 0
        for (i in 0 until player0RackUpdated.size) {
            val plTile = player0RackUpdated[i]
            player0Rack[j].visual = colorToVisual(plTile.firstColor)
            player0Rack[j + 1].visual = colorToVisual(plTile.secondColor)
            j += 2
        }

        // For player 1
        val player1RackUpdated = gameState.players[1].rack
        player1label.text = gameState.players[1].name + "'s Stats"
        player1label.isVisible = true
        for (visTile in player1Rack) {
            visTile.visual = ColorVisual.TRANSPARENT
        }
        j = 0
        for (i in 0 until player1RackUpdated.size) {
            val plTile = player1RackUpdated[i]

            player1Rack[j].visual = colorToVisual(plTile.firstColor)
            player1Rack[j + 1].visual = colorToVisual(plTile.secondColor)
            j += 2
        }




        if (playerCount <= 2)
            return
        // For player 2
        val player2RackUpdated = gameState.players[2].rack
        player2label.text = gameState.players[2].name + "'s Stats"
        player2label.isVisible = true
        for (visTile in player2Rack) {
            visTile.visual = ColorVisual.TRANSPARENT
        }
        j = 0
        for (i in 0 until player2RackUpdated.size) {
            val plTile = player2RackUpdated[i]

            player2Rack[j].visual = colorToVisual(plTile.firstColor)
            player2Rack[j + 1].visual = colorToVisual(plTile.secondColor)
            j += 2
        }





        if (playerCount <= 3)
            return
        // For player 3
        val player3RackUpdated = gameState.players[3].rack
        player3label.text = gameState.players[3].name + "'s Stats"
        player3label.isVisible = true
        for (visTile in player3Rack) {
            visTile.visual = ColorVisual.TRANSPARENT
        }
        j = 0
        for (i in 0 until player3RackUpdated.size) {
            val plTile = player3RackUpdated[i]

            player3Rack[j].visual = colorToVisual(plTile.firstColor)
            player3Rack[j + 1].visual = colorToVisual(plTile.secondColor)
            j += 2
        }
    }

    override fun refreshConnectionState(connectionState: ConnectionState) {
        if (connectionState == ConnectionState.DISCONNECTED) {
            pauseButton.apply {
                onMouseClicked = {
                    application.refreshAfterPause()

                }
            }
            game.isNetworkGame = false
            rootService.networkService.disconnect()
            rootService.gameService.endGame()
        }
    }
}
