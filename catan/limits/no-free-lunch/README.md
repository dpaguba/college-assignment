# No free lunch, computed

The theorem is usually quoted. Here it is enumerated: five points, so 32
possible target functions, three of them seen during training and two held
back. Six learners, deliberately different from each other.

| learner | average error on the unseen points |
|---|---:|
| majority | 0.5 |
| against the majority | 0.5 |
| always zero | 0.5 |
| always one | 0.5 |
| nearest seen point | 0.5 |
| alternating | 0.5 |

Exactly one half, every one of them, to twelve decimals. The same holds for
four points with one seen, five with two, and six with four.

## Why

For every target function there is a second one that agrees on the seen points
and disagrees on every unseen point. Whatever a learner gains on the first it
loses on the second, and the pairing does not care how the learner is built.

## And why it does not mean what it is usually taken to mean

On a single target the learners are far apart. On a smooth one, half zeros
then half ones:

| learner | error |
|---|---:|
| against the majority | 0.00 |
| alternating | 0.33 |
| majority | 1.00 |

The averaging is where the theorem gets its force, and it is also where it
loses its relevance: real problems are not a uniform draw from all possible
functions. They are smooth, structured and repetitive.

So the theorem is not a reason to treat methods as interchangeable. It is a
demand to say out loud which assumption makes a method good. For the project
that is concrete: an AI is built for Catan, not for board games in general,
and what makes it good at Catan is exactly the assumptions about Catan baked
into it.
