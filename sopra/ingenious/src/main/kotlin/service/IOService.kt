package service

import entity.Game
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString
import tools.aqua.bgw.visual.ImageVisual
import java.io.File
import java.io.IOException
import java.lang.IllegalArgumentException
import java.nio.file.Path
import kotlin.io.path.Path

/**
 * The IOService can be used to store and load games in/from three "slots".
 *
 * The slots have numbers from 0 to 2. Some slots have a preview image.
 * To get a list of all slots, their state (full/empty) and their preview, call [getSavedGames].
 * Storing and loading is done with [storeGame] and [loadGame].
 *
 * @param rootService is the root service of the game. It is used to get/set the current game.
 */
class IOService(private val rootService: RootService) : AbstractRefreshingService() {
    private val defaultPath = "./slots/" // The path
    private val defaultFileNamePrefix = "slot" // This is the filename prefix. It is followed by a number
    private val defaultFilenameExtension = ".ingeniousFile" // this is the last part of the filename

    /**
     * This function will provide you with all the information needed to show a saved games selection menu.
     *
     * @return an array of pairs containing a string (first) and an image visual (second). The string is the
     * filename of the saved game. If this is empty, you can assume that the slot is empty.
     * The image visual is a screenshot of the game state.
     * Please use the position of the items in the arrays as "slot" number when loading or storing a game.
     */
    fun getSavedGames(): Array<Pair<String, ImageVisual?>> {
        val result: Array<Pair<String, ImageVisual?>> = Array(3, init = { Pair("", null) })

        // get the saved slot paths
        val slots: Array<Path> = Array(3, init = { Path("") })
        slots[0] = Path("$defaultPath${defaultFileNamePrefix}0$defaultFilenameExtension")
        slots[1] = Path("$defaultPath${defaultFileNamePrefix}1$defaultFilenameExtension")
        slots[2] = Path("$defaultPath${defaultFileNamePrefix}2$defaultFilenameExtension")

        // Try to open the paths and reset those that are not readable
        for (i in 0..2) {
            if(!File("${slots[i]}").exists()) {
                slots[i] = Path("")
            }
        }

        // fill the result array
        for (i in 0..2) {
            //get an image for the scene
            val image: ImageVisual? = try {
                ImageVisual("${slots[i].fileName}.vis")
            } catch (e: IllegalArgumentException){
                // Getting detect to accept that I do not want to do anything with this exception
                val ex = e.toString()
                ex.trim()
                null
            }
            //set the filename
            val slotPair = Pair(slots[i].fileName.toString(), image)
            result[i] = slotPair
        }
        return result
    }

    /**
     * This function stores the current game on the devices mass storage.
     *
     * @param slot must be a number between 0 and 2. This is the storage slot to store to.
     *
     * @throws SecurityException if the security manager does not allow the creation of the file
     */
    fun storeGame(slot: Int) {
        if (slot !in 0..2)
            throw IllegalArgumentException("This slot does not exist!")
        // Create the directory if it does not exist
        val directory = File(defaultPath)
        if (!directory.exists()) {
            // create it (change to mkdirs if the game state directory path is multiple dirs deep!)
            directory.mkdir()
        }
        //val game = rootService.game

        //val newGame = Game(game.isNetworkGame, game.isTeamMode)
        //newGame.currentGameState = game.createNextGameState()
        //newGame.currentGameState.nextGameState = null
        //newGame.currentGameState.prevGameState = null
        //if(game.hasPrevGameState())
            //game.currentGameState = game.switchPrevGameState()

        // serialize the current game
        val serializedGame = Json.encodeToString(rootService.game)

        // get a file pointer and write the file
        val gameFile = File("$defaultPath$defaultFileNamePrefix$slot$defaultFilenameExtension")
        gameFile.writeText(serializedGame)
    }

    /**
     * This function retrieves a previously saved game from the devices mass storage.
     *
     * @param slot must be a number between 0 and 2. This is the storage slot to load from.
     *
     * @throws NoSuchElementException if the slot does not exist
     * @throws IllegalArgumentException if the slot number is wrong
     */
    fun loadGame(slot: Int) {
        if (slot !in 0..2)
            throw IllegalArgumentException("This slot does not exist!")

        val slots = getSavedGames()
        if (slots[slot].first == "")
            throw NoSuchElementException("The slot is empty!")

        // get the file content:
        val inputStream = File("${defaultPath}${slots[slot].first}").inputStream()
        val serializedClass = inputStream.bufferedReader().use { it.readText() }
        // check if the string is empty
        if (serializedClass == "") {
            throw IOException("This slot is corrupted. I'm sorry ):")
        }
        // load and set the game object
        val loadedGame = Json.decodeFromString<Game>(serializedClass)
        //Jason to java: activates the game constructor, therefore we need to delete the last entry GameStateList and
        // set the current game
        loadedGame.gameStateList.removeLast()
        loadedGame.currentGameState = loadedGame.gameStateList.last()
        // now load the game for real
        rootService.game = loadedGame
        onAllRefreshables { refreshAfterLoadGame() }
    }
}