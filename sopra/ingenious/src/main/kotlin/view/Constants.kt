package view

import entity.PlayerType
import tools.aqua.bgw.util.Font
import java.awt.Color

/**
 * This package contains visual constants and settings for creating a user interface in Kotlin applications.
 * It focuses on defining visual elements such as button styles, font settings, and player types for an improved user
 * experience.
 */

val BACKGROUND_COLOR = Color(35, 55, 100)

// Button Dimensions
const val HEIGHT_BUTTON: Int = 90  // The height of buttons in pixels.
const val WIDTH_BUTTON: Int = 500   // The width of buttons in pixels.
val BACKGROUND_COLOR_BUTTON = Color(217, 217, 217)

// Button Font
val FONT_BUTTON: Font = Font(       // The font used for buttons.
    color = Color.BLACK,
    fontStyle = Font.FontStyle.NORMAL,
    fontWeight = Font.FontWeight.BOLD,
    size = 36
)

// Title Dimensions
const val HEIGHT_TITLE: Int = 150   // The height of title elements in pixels.
const val WIDTH_TITLE: Int = 600    // The width of title elements in pixels.
val FONT_TITLE: Font = Font(       // The font used for titles.
    color = Color.WHITE,
    fontStyle = Font.FontStyle.NORMAL,
    family = "Hanuman",
    fontWeight = Font.FontWeight.BOLD,
    size = 100
)

/**
 * List of available player types.
 *
 * This list contains the different types of players that can participate in the game.
 */
val PLAYER_TYPES_LIST: List<PlayerType> = listOf(
    PlayerType.LOCAL,
    //PlayerType.NETWORK,
    PlayerType.AI,
    PlayerType.AI_RANDOM
)

/**
 * The font used for displaying player names in the player list.
 */
val FONT_PLAYERLIST = Font(
    color = Color.BLACK,
    fontStyle = Font.FontStyle.NORMAL,
    fontWeight = Font.FontWeight.BOLD,
    size = 36
)