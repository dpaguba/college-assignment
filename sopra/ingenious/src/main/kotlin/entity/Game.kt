package entity

import kotlinx.serialization.Serializable

/**
 * This class is the main reference point to the entity classes.
 *
 * It serves as the main pointer to the "list of gamestates"
 * On Creation, it creates a dummy gameState with null pointers and empty lists
 *
 * @property isNetworkGame signalizes if this is a hotseat game or the online variation
 * @property isTeamMode signalizes if this is an FFA game or the variation vor 4 Players where 2 play in one Team
 * @property currentGameState is a reference to the current game can be null
 */
@Serializable
data class Game(var isNetworkGame: Boolean, var isTeamMode: Boolean) {

    var currentGameState : GameState
    var currentGameStateIndex = 0
    var gameStateList = mutableListOf<GameState>()
    init{
        //create a dummy gameState with an empty bag and no players
        currentGameState  = GameState(0,
            null,
            null,
            mutableListOf(),
            mutableListOf(),
            Board(5)
        )
        gameStateList.add(currentGameState)
    }

    /**
     * Tests if the currentGameState has a next PlayState(2 in advance)
     *
     * @return true if it exists / false if null
     * @throws NullPointerException, if the currentGameState is null
     */
    fun hasNextGameState() : Boolean{
        return currentGameStateIndex < gameStateList.size
    }

    /**
     * Tests if the currentGameState has a previous PlayState(2 behind)
     *
     * @return true if it exists / false if null
     * @throws NullPointerException, if the currentGameState is null
     */
    fun hasPrevGameState() : Boolean{
        return currentGameStateIndex-2 > 0
    }

    /**
     * Returns the previous playState and changes the currentGameState(Index)
     *
     * @return previousGamestate
     * @throws IllegalStateException if no previous exists
     */
    fun switchPrevGameState() : GameState {
        if(hasPrevGameState() && currentGameStateIndex - 2 >= 0){
            currentGameStateIndex -= 2
            currentGameState = gameStateList[currentGameStateIndex]
            return currentGameState
        }
        //else just give the safe state back
        throw IllegalStateException("we only have one state left. make a copy of its stuff to yout state")
    }

    /**
     * Returns the next playState and changes the currentGameState(Index)
     *
     * @return nextGameState
     * @throws IllegalStateException if no next exits
     */
    fun switchNextGameState() : GameState{
        if(hasNextGameState() && currentGameStateIndex+2 <= gameStateList.size){
            currentGameStateIndex += 2
            currentGameState = gameStateList[currentGameStateIndex]
            return currentGameState
        }
        throw IllegalStateException("We have no future left.")

    }

    /**
     * Creates a new GameState based on the current one.
     *
     * for test team check test if tiles get copied by exhanging a players left most tile and test if they are now
     * NOTEQUAL. same for scoreboard and board.
     * the new one gets filled with new objects based on the old ones. CurrentPlayer STAYS THE SAME.
     * like everything else
     * @return the new current gameState
     */
    fun createNextGameState() : GameState {
        /*
            .copy() makes a copy of current object, but deeper objects are only given as a reference
            Therefore it is needed to build the copies from the ground up
         */
        val current = currentGameState

        //create copies of the objects in current gamestate
        val newPlayerList: MutableList<Player> = copyPlayerList()
        val newBag = copyBag()
        val newBoard = copyBoard()
        // create the new gameState
        val newGameState = GameState(
            current.currentPlayerIndex,
            null,
            null,
            newBag,
            newPlayerList,
            newBoard
        )
        if(gameStateList.size>currentGameStateIndex+1){
            gameStateList.dropLast(gameStateList.size-currentGameStateIndex)
        }
        gameStateList.add(newGameState)
        currentGameStateIndex++
        currentGameState = newGameState
        return currentGameState

    }

    /**
     * A private function, that copies all player objects
     *
     * @return the list of all players, that are in the current gamestate
     */
    private fun copyPlayerList(): MutableList<Player> {
        val current = currentGameState
        val newPlayerList = mutableListOf<Player>()
        //create new player objects
        for(player in current.players){
            val newPlayer = Player(player.name,player.type)
            newPlayer.isInFirstRound = player.isInFirstRound
            newPlayer.remainingRounds = player.remainingRounds
            //copy all tiles from rack .copy() might be a bit overkill
            for(tile in player.rack){
                newPlayer.rack.add(tile.copy())
            }

            for(pair in player.scoreBoard){
                newPlayer.scoreBoard[pair.key] = pair.value
            }
            newPlayerList.add(newPlayer)
        }

        //sync the scoreBoards in teamGame
        if(isTeamMode && newPlayerList.size == 4){
            newPlayerList[2].scoreBoard = newPlayerList[0].scoreBoard
            newPlayerList[3].scoreBoard = newPlayerList[1].scoreBoard
        }
        return newPlayerList
    }

    /**
     * A private function, that copies the draw bag
     *
     * @return a copy of Bag
     */
    fun copyBag(): MutableList<Tile> {
        //maybe it is enough to just call bag.copy(), but this is safe
        val current = currentGameState
        val newBag = mutableListOf<Tile>()
        for(tile in current.bag){
            newBag.add(tile.copy())
        }
        return newBag
    }

    /**
     * A private function, that copies the board
     *
     * @return a copy of Board
     */
    private fun copyBoard(): Board{
        val current = currentGameState
        val newBoard = current.board.copy()
        //copy the fields arraylist to a new one
        val newField = arrayListOf<ArrayList<TileColor>>()
        for (list in current.board.fields){
            val nList = arrayListOf<TileColor>()
            for((i,color) in list.withIndex()){
                nList.add(i,color)
            }
            newField.add(nList)
        }
        //override the fields-list with a new fields-list
        newBoard.fields = newField
        return newBoard
    }
}
# Modified 2025-08-11 10:24:31