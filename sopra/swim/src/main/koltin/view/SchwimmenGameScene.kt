package view

import service.CardImageLoader
import service.SchwimmenService
import tools.aqua.bgw.components.gamecomponentviews.CardView
import tools.aqua.bgw.components.uicomponents.Button
import tools.aqua.bgw.components.uicomponents.Label
import tools.aqua.bgw.core.Alignment
import tools.aqua.bgw.core.BoardGameScene
import tools.aqua.bgw.util.Font
import tools.aqua.bgw.visual.ColorVisual
import tools.aqua.bgw.visual.ImageVisual

class SchwimmenGameScene(private val schwimmenService: SchwimmenService) :
        BoardGameScene(1900, 1080), Refreshable {
    val swapAllButton =
            Button(
                            posX = 20,
                            posY = 600,
                            width = 200,
                            height = 70,
                            text = "Swap All",
                            font = Font(size = 30)
                    )
                    .apply { visual = ColorVisual(150, 75, 0) }

    val swapOneButton =
            Button(
                            posX = 20,
                            posY = 690,
                            width = 200,
                            height = 70,
                            text = "Swap One",
                            font = Font(size = 30)
                    )
                    .apply {
                        visual = ColorVisual(150, 75, 0)
                        onMouseClicked = {
                            this.isVisible = false
                            confirmButton.isVisible = true
                            swapAllButton.isVisible = false
                            passButton.isVisible = false
                            knockButton.isVisible = false
                            val handCards = mutableListOf(handCard1, handCard2, handCard3)
                            val middleCards = mutableListOf(middleCard1, middleCard2, middleCard3)
                            var handCardsIndex = handCards.size
                            var middleCardsIndex = middleCards.size

                            for (handCard in handCards) {
                                handCard.onMouseClicked = {
                                    for (handCardSub in handCards) {
                                        handCardSub.scale = 1.0
                                    }
                                    handCard.scale = 1.1
                                    handCardsIndex = handCards.indexOf(handCard)
                                }
                            }

                            for (middleCard in middleCards) {
                                middleCard.onMouseClicked = {
                                    for (middleCardSub in middleCards) {
                                        middleCardSub.scale = 1.0
                                    }
                                    middleCard.scale = 1.1
                                    middleCardsIndex = middleCards.indexOf(middleCard)
                                }
                            }
                            confirmButton.onMouseClicked = {
                                if (handCardsIndex < handCards.size &&
                                                middleCardsIndex < middleCards.size
                                ) {
                                    val game = schwimmenService.currentGame
                                    val middle = schwimmenService.middle
//                                    checkNotNull(game)
                                    schwimmenService.playerService.swapOne(
                                            game.currentPlayer.hand[handCardsIndex],
                                            middle.middle[middleCardsIndex]
                                    )
                                    for (handCard in handCards) {
                                        handCard.scale = 1.0
                                        handCard.onMouseClicked = {}
                                    }
                                    for (middleCard in middleCards) {
                                        middleCard.scale = 1.0
                                        middleCard.onMouseClicked = {}
                                    }
                                    this.isVisible = true
                                    confirmButton.isVisible = false
                                    swapAllButton.isVisible = true
                                    passButton.isVisible = true
                                    knockButton.isVisible = true
                                }
                            }
                        }
                    }

    // button to confirm swap one
    val confirmButton =
            Button(
                            posX = 20,
                            posY = 690,
                            width = 200,
                            height = 70,
                            text = "Confirm",
                            font = Font(size = 30)
                    )
                    .apply {
                        visual = ColorVisual(150, 75, 0)
                        this.isVisible = false
                    }

    val passButton =
            Button(
                            posX = 1700,
                            posY = 600,
                            width = 200,
                            height = 70,
                            text = "Pass",
                            font = Font(size = 30)
                    )
                    .apply { visual = ColorVisual(150, 75, 0)
                    }

    val knockButton =
            Button(
                            posX = 1700,
                            posY = 690,
                            width = 200,
                            height = 70,
                            text = "Knock",
                            font = Font(size = 30)
                    )
                    .apply {
                        visual = ColorVisual(150, 75, 0)
                        onMouseClicked = { schwimmenService.playerService.knock() }
                    }

    val cardImageLoader = CardImageLoader()

    private val handCardsLabel =
            Label(
                    posX = 700,
                    posY = 750,
                    width = 530,
                    height = 50,
                    text = "Hand cards",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER
            )

    private var handCard1 =
            CardView(
                    posX = 700,
                    posY = 800,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage),
            )

    private var handCard2 =
            CardView(
                    posX = 900,
                    posY = 800,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private var handCard3 =
            CardView(
                    posX = 1100,
                    posY = 800,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private val middleCardsLabel =
            Label(
                    posX = 700,
                    posY = 350,
                    width = 530,
                    height = 50,
                    text = "Table cards",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER
            )

    private var middleCard1 =
            CardView(
                    posX = 700,
                    posY = 400,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private var middleCard2 =
            CardView(
                    posX = 900,
                    posY = 400,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private var middleCard3 =
            CardView(
                    posX = 1100,
                    posY = 400,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private val drawStackLabel =
            Label(
                    posX = 20,
                    posY = 120,
                    width = 130,
                    height = 20,
                    text = "Draw stack",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER_LEFT
            )

    private var drawStack =
            CardView(
                    posX = 20,
                    posY = 160,
                    front = ImageVisual(cardImageLoader.backImage),
                    back = ImageVisual(cardImageLoader.backImage)
            )

    private var drawStackCardsAmount =
            Label(
                    posX = 20,
                    posY = 360,
                    width = 200,
                    height = 20,
                    text = "Left: ",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER_LEFT
            )

    private var currentPlayerName =
            Label(
                    posX = 20,
                    posY = 20,
                    width = 400,
                    height = 70,
                    text = "",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER_LEFT
            )

    private var knockStatus =
            Label(
                    posX = 1500,
                    posY = 20,
                    width = 400,
                    height = 70,
                    text = "No one has knocked",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER_RIGHT
            )

    private var passCounter =
            Label(
                    posX = 1500,
                    posY = 110,
                    width = 400,
                    height = 70,
                    text = "",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER_RIGHT
            )

    private var playerScore =
            Label(
                    posX = 700,
                    posY = 1000,
                    width = 530,
                    height = 50,
                    text = "Score: ",
                    font = Font(size = 30),
                    alignment = Alignment.CENTER
            )
    init {
        background = ColorVisual(108, 168, 59)

        addComponents(
                swapAllButton,
                swapOneButton,
                passButton,
                knockButton,
                confirmButton,
                handCardsLabel,
                playerScore,
                handCard1,
                handCard2,
                handCard3,
                middleCardsLabel,
                middleCard1,
                middleCard2,
                middleCard3,
                currentPlayerName,
                knockStatus,
                passCounter,
                drawStackLabel,
                drawStack,
                drawStackCardsAmount
        )
    }

    // Universal function to refresh all the GUI
    private fun refreshGUI() {
        val game = schwimmenService.currentGame
        val middle = schwimmenService.middle
        val drawStack = schwimmenService.drawStack
        //        checkNotNull(game)

        handCard1.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                game.currentPlayer.hand[0].suit,
                                game.currentPlayer.hand[0].value
                        )
                )
        handCard2.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                game.currentPlayer.hand[1].suit,
                                game.currentPlayer.hand[1].value
                        )
                )
        handCard3.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                game.currentPlayer.hand[2].suit,
                                game.currentPlayer.hand[2].value
                        )
                )

        handCard1.showFront()
        handCard2.showFront()
        handCard3.showFront()

        playerScore.text = "Score: ${game.currentPlayer.score}"

        middleCard1.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                middle.middle[0].suit,
                                middle.middle[0].value
                        )
                )
        middleCard2.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                middle.middle[1].suit,
                                middle.middle[1].value
                        )
                )
        middleCard3.frontVisual =
                ImageVisual(
                        cardImageLoader.frontImageFor(
                                middle.middle[2].suit,
                                middle.middle[2].value
                        )
                )

        middleCard1.showFront()
        middleCard2.showFront()
        middleCard3.showFront()

        currentPlayerName.text = " ${game.currentPlayer.name}'s turn"
        passCounter.text = "Pass Counter: ${game.passCounter}"

        val knockedPlayer = game.players.firstOrNull { it.hasKnocked }
        if (knockedPlayer != null) knockStatus.text = "${knockedPlayer.name} has knocked"
        else knockStatus.text = "No one has knocked"

        drawStackCardsAmount.text = "Left: ${drawStack.drawStack.size}"
    }

    override fun refreshAfterStartGame() = refreshGUI()

    override fun refreshAfterCardChange() = refreshGUI()

    override fun refreshAfterTurn() = refreshGUI()
}
