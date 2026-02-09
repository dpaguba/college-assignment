# AutoML

| Module | Topic |
|---|---|
| [gaussian-process](gaussian-process/) | the model with an error bar |
| [expected-improvement](expected-improvement/) | where to measure next |
| [bayesian-optimisation](bayesian-optimisation/) | the loop, against the baselines |
| [successive-halving](successive-halving/) | budget instead of full runs |
| [tuning-bias](tuning-bias/) | the price of trying many things |

On 25 evaluations the loop reaches a regret of 0.0000016 where a grid of the
same size reaches 0.0097 and random search 0.0537. At 120 evaluations the
advantage is gone, which is the statement of what the method is for.

The last module is the counterweight: trying 500 configurations that are all
equally good and reporting the best inflates the number by 0.041, and the
size of that inflation is predictable in advance from the expected maximum of
k normal variables.
