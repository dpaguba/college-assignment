# Current Problems
 - GUI is not very verbose in what to do
 - Add Decline Action to GUI
 - 

# Trading
  Player to player trading is implemented in a way that an active player can create a trade request that contains the target player and what resources he would like to trade. The target player gets the request to accept or pass on the trade. 
## Example:
 - TradeAction(my_player_no, other_player_no, np.array(1,0,0,1,0,2), np.array(0,2,0,0,0,2)) exchanges one wood and one ore against tow clay


# Developing an AI for Settlers of Catan

## Changes to game rules
- The resources of each player will stay visible (counting would be pretty accurate too, but there is no point in everybody implementing an approximation algorithm.)
- For Progress Cards, only the total number of them will be visible for other players.

## Programming
- The game, as it is, should be usable with any OS and Python version between 3.10 and 3.13.
- Most of the functions have type annotations. You can turn on the type checker to get hints of what data they expect.
- The AI Player Class in your team folder contains all the data you need to implement the handle_request(self, message_type: MessageType, possible_actions: list[Action]) -> Action function.
- Your helper functions should go in that class or in their own module so it can be used by both your AI's.
- To use your AI, create one player of the corresponding AI class in a copy of one of the example execution scripts.

### Logging
- Logging of the game actions can be enabled when creating the LearnLettlers class.
- In that case, the result of every turn will be saved in a file in the gamelogs folder and all can be reassembled to generate training data.
- The second log is used for logging the network traffic or other internal systems and should not be necessary to use.

### debugging
- In case something unexpected happens, feel free to debug the code. This works best with the basic AI only execution like in ai_play_learn_settlers.py.
- Or watch what happens with the GUI.

## Game execution
- For AI development, replace one of the RandomPlayers in any of the following scripts with your AI player.
- ai_play_learn_settlers.py: example of an AI only local game
- local_play_learn_settlers.py: example of a game with one UI
- client_play_learn_settlers.py: creates one client that connects to the server, joins game 0 and then starts the game. Best used after other players did join.
- human_client_play_learn_settlers.py: connects an UI client to a server.
- multiple_clients.py: connects multiple AI clients to a server.
- server_learn_settlers.py: starts a server, that can host multiple matches at the same time.
- all the test scripts are only for testing the game logic an should not be useful for the AI development.

## Data extraction from logs
- Create an instance of a log_reader, and use the generate_game_states method to generate a list of all game states that existed in the original game.
