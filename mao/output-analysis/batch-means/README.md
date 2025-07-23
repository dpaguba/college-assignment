# Batch means

One long run turned into a few nearly independent observations.

On a queue at 80 percent load over 20 000 arrivals:

| | |
|---|---:|
| correlation between consecutive observations | 0.962 |
| correlation between 20 batch means | -0.072 |
| half width from the batch means | 0.546 |
| half width ignoring the correlation | 0.065 |

The naive interval is eight times too narrow. That is the number worth
carrying out of the whole output analysis chapter: treating simulation output
as independent does not make the interval slightly optimistic, it makes it
wrong by an order of magnitude.

The trade is between the number of batches and their length. Few long batches
are nearly independent and give a wide interval because there are few of
them; many short ones are still correlated and give an interval that is too
narrow again. The module reports the correlation of the batch means so the
choice rests on evidence.
