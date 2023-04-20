import glob,  pandas as pd, plotly.graph_objects as go
import cProfile

from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ui.ui_player import UIPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.ui.display import Display
from ai_games.learn_settlers.utils.log_reader import LogReader
from ai_games.learn_settlers.utils.message_tester import MessageTester

def main():
    result_list = []
    for file in glob.glob("gamelog/*.gz"):
        log_reader = LogReader(file)
        # game_states = log_reader.generate_game_states()
        # turn_game_states = log_reader.generate_game_states_per_turn(game_states)
        result_list.append(log_reader.res)
    results = pd.DataFrame(result_list)

    results.rename(columns={"player_Reference":"Reference",
                    "Player_random":"Random",
                    "team1":"Team 1",
                    "team2":"Team 2",
                    "team3":"Team 3",
                    "team4":"Team 4",
                    "team5":"Team 5",
                    "team6":"Team 6",
                    }, inplace=True)

    print("mean points per player:")
    mean_res = results.mean(axis=0)
    mean_res.sort_values(inplace=True,ascending=False)
    print(mean_res)
    print("median points per player:")
    median_res = results.median(axis=0)
    median_res.sort_values(inplace=True,ascending=False)
    print(median_res)
    print("wins per player:")
    win_count = results.idxmax(axis=1, skipna=True,numeric_only=True).value_counts()
    win_count.sort_values(inplace=True,ascending=False)
    win_rate = win_count/sum(results.iloc[:,0].notna())
    print(win_count)

    fig = go.Figure(go.Bar(y=mean_res, x = mean_res.index))
    fig.update_layout(xaxis_title="Player", yaxis_title="Average Points", title=f"Average Points")
    fig.show()

    fig = go.Figure(go.Bar(y=median_res, x = median_res.index))
    fig.update_layout(xaxis_title="Player", yaxis_title="Median Points", title=f"Median Points")
    fig.show()

    fig = go.Figure(go.Bar(y=win_count, x = win_count.index))
    fig.update_layout(xaxis_title="Player", yaxis_title="Win Count", title=f"Win Count")
    fig.show()

    fig = go.Figure(go.Bar(y=win_rate, x = win_rate.index))
    fig.update_layout(xaxis_title="Player", yaxis_title="Win Rate", title=f"Win Rate")
    fig.show()


if __name__ == "__main__":
    # cProfile.run("main()", sort="cumtime")
    main()