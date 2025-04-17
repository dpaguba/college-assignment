# Choosing a move

| Module | Topic |
|---|---|
| [move-generation](move-generation/) | what is legal, and how much fits |
| [scoring-function](scoring-function/) | the weighted sum and its ceiling |
| [one-ply-vs-two-ply](one-ply-vs-two-ply/) | when looking further hurts |
| [expectimax](expectimax/) | deciding against the dice |

The slides ask four questions about the AI: what the goal is, what separates a
good move from a bad one, when to end a turn, and how far it pays to look
ahead. This block answers the last two with numbers.

Two results cut against the intuition. A weighted sum of features cannot
prefer a balanced corner over two extreme ones, whatever the weights, and a
grid of 4 225 weight vectors confirms it. And a two-ply search with an
imperfect evaluation function picks a move worth 0 where the one-ply search
picks the one worth 10.
