# Rejecting instead of guessing

Sort by confidence, cut from the bottom, and measure the error on what is
left. If the confidence is worth anything the error falls; if it is not, it
stays.

| coverage | risk |
|---:|---:|
| 5 % | **0.005** |
| 100 % | 0.265 |

## The check needs no ground truth for the uncertainty

Two models that predict the same things and are wrong equally often. One knows
when it is wrong, the other does not:

| | real confidence | random confidence |
|---|---:|---:|
| risk at half coverage | **0.133** | 0.255 |
| risk at full coverage | 0.265 | 0.257 |
| area under the curve | **0.135** | 0.253 |

There is no such thing as the true uncertainty of a case to compare against.
What can be checked is the effect: sorted by the estimate, the errors should
come first. The curve measures that using only the labels that already exist.

## Where to cut is a different question

A rejected prediction has to be handled by a person, and that costs something:

| cost of a rejection | best coverage |
|---:|---:|
| 0.05 | **10 %** |
| 0.6 | **100 %** |

The curve says how good the confidence is. It does not say where to cut, and
nothing in the data does.
