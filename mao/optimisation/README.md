# Optimisation

| Topic | |
|---|---|
| [convexity](convexity/) | what makes a problem tractable |
| [linear-programming](linear-programming/) | the optimum is a vertex |
| [duality](duality/) | shadow prices |
| [integer-programming](integer-programming/) | the bound, and the greedy warning |
| [dynamic-programming](dynamic-programming/) | one decision at a time |
| [heuristics](heuristics/) | an answer without a bound |

Chapters nine to twelve. The tenth sheet's production problem runs through
the first three modules: the optimum is 300 and 150 for a profit of 1500,
the machine hours and the raw material are exhausted, and their shadow prices
are 0.5 and 0.3 while the slack market constraint is worth nothing.

The block's two measured results are about the cost of exactness. Branch and
bound explores 5 nodes where enumeration explores 961, and memoisation turns
21 891 recursive calls into 39. Both are the same idea: the structure of the
problem is what makes it solvable, and using it is the whole method.
