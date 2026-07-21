# Importance by shuffling

Shuffle a column, so its relationship with the target is destroyed while its
distribution survives, and measure how much worse the model gets.

For a linear model the answer is known in closed form: the increase is
`2·β̂ⱼ²·Var(xⱼ)`. The implementation is checked against it, which is a stronger
test than any comparison between two shuffling implementations.

## What a duplicated feature does

The same feature appears twice in the data:

| | importance |
|---|---:|
| the feature on its own | **7.98** |
| each of the two copies | **2.00** |

Exactly a quarter, because the weight is split in half and the error is
quadratic. Both copies look unimportant while the feature explains everything.
Dropping one copy changes the error by nothing at all, to fifteen digits.

This is not a corner case. With strongly correlated features the same effect
appears in a weaker form, and the ranking then says more about the
relationships among the features than about their importance.

## The number is about the model, not the data

The same feature, two models, one that uses it and one that ignores it:

| | importance |
|---|---:|
| the model that uses it | **2.00** |
| the model that ignores it | **0.00** |

The number answers "what does this model lean on", not "what is in the data".
Reading it as a statement about the world confuses two different questions,
and with a poor model it misleads reliably.

## What helps

Shuffling groups of related features together rather than one at a time,
asking beforehand which of the two questions is being asked, and measuring on
held-out data. On the training data one also measures whatever the model has
memorised.
