# Generating the legal moves

A settlement blocks its own corner and every neighbouring corner, so one piece
removes up to four places from the board. Roads must connect to the player's
own network, which is why the game starts by placing two settlements: with
nothing on the board, no road is legal.

## How many settlements fit

The largest set of corners no two of which are adjacent is the maximum
independent set of the intersection graph. Branch and bound over bitmasks
gives **27**, exactly half of the 54 corners.

The box holds 20 settlements for four players. So the distance rule is not
what limits the board; the pieces are, and in a real game the roads needed to
reach a far corner bind earlier still.

The answer is checked three ways: the returned set really is independent, no
corner can be added to it, and 4 000 randomised greedy runs never find more
than 27.

## Where the real work is

The project's game implementation offers all legal moves for most turns, and
the task is to pick the best. The two exceptions say something: a trade offer
has to be constructed by the asking player, and the cards to discard have to
be chosen. Both are exactly the places where the space cannot be enumerated,
the trade offers because there is no bound on them and the discard sets
because they grow with the hand.
