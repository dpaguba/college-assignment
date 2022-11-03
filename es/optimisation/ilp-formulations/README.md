# Integer linear programming

Assignment, scheduling and allocation are the same shape: a zero-one variable
per pair, linear constraints, a linear cost. Writing the problem that way
separates the model from the solver, which is the point of the lecture's
session on it.

The formulation is short. One equality per task saying it is placed exactly
once, one inequality per processor for its capacity, and a sum for the cost.
The solving is what costs: assignments of four tasks to three processors
number 81, and the count is exponential in the tasks.

The linear relaxation gives a lower bound cheaply, and the module computes
both so the gap can be seen. When the capacities do not bind, the relaxation
is exact and the integer problem was never needed; when they do, the gap is
what the search has to close.
