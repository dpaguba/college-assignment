# Uncertainty

| Module | Topic |
|---|---|
| [calibration](calibration/) | do the numbers mean what they say |
| [aleatoric-and-epistemic](aleatoric-and-epistemic/) | which part more data remove |
| [reject-option](reject-option/) | checking an estimate by its effect |
| [conformal-prediction](conformal-prediction/) | a guarantee that ignores the model |
| [soft-labels](soft-labels/) | what the majority vote discards |

Several of the offers ask for an uncertainty method to be benchmarked, which
raises the question of what a benchmark for uncertainty even is: the true
uncertainty of a case is written nowhere. Three answers appear here. Check the
probabilities against the observed frequencies, check the ranking by its
effect on the error when the hardest cases are dropped, or get a measured
uncertainty from crowd votes.

The verification found one check in this block that was not a check: the
identity total = noise + disagreement holds by construction, because the
second part is computed as the remainder. Both parts are recomputed
independently now.
