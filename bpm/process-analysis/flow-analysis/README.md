# Flow analysis

The cycle time of a block-structured model, computed by recursion over four
block types plus the loop:

| Block | Cycle time |
|---|---|
| sequence | sum of the parts |
| exclusive choice | Σ pᵢ · Tᵢ |
| parallel | max of the branches |
| loop | T / (1 − r) |
| inclusive | Σ p_case · max over the branches of that case |

The inclusive block is the one the formula sheet does not give. Zettel 4
states it as three cases with their probabilities: 10 % only new features,
30 % only bug fixes, 60 % both. That is exactly the shape the code takes, and
it is a better fit than independent per-branch probabilities, because the
sheet gives the probabilities of the combinations and not of the branches.

## The exercises

| Model | Cycle time |
|---|---|
| Loan application | 1 + max(1,3) + 3 + (0.6·1 + 0.4·2) = **8.4 days** |
| The same with a 20 % rework loop on the first check | **8.65 days** |
| App release | 4 + (0.1·24 + 0.3·6 + 0.6·24) + 2 = **24.6 hours** |
| Application form | 10 + 1.2 + 15 + 10 + max(2,5) = **41.2 minutes** |
| Exposé | 2 + 4 + 1.25·2 = **8.5 days** |

## Two checks

`simulate` plays single cases and averages them, which is the check that the
recursion picks branches the way the model says. The stronger check is
exhaustive enumeration over every combination of branches, weighted by
probability: that is the exact expectation, and it agrees with the formula
for all five models above.

`work_time` runs the same recursion with processing times instead of cycle
times. The parallel block takes the maximum there too, which is what the
formula sheet prescribes and what the efficiency module then divides by.
