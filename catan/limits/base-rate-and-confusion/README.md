# The base rate

## Guessing the majority

With 99 % of cases in one class, always answering that class scores:

| | |
|---|---:|
| accuracy | **0.99** |
| balanced accuracy | 0.50 |
| recall of the rare class | 0.00 |

Nothing was learned, and one of the three numbers says so.

## What a positive result is worth

A test with 99 % sensitivity and 99 % specificity, on a condition present in
1 % of people. Per 10 000 people: 99 true positives and 99 false alarms, so a
positive result is right **half** the time. At a prevalence of 0.1 % it is
right 9 % of the time.

The quality of the test did not change. The base rate did, and it dominates.

## Why this is the central number for a game AI

Most moves in a game are of no consequence. A model that learns to tell good
moves from bad therefore works on a heavily skewed distribution, and 95 %
accuracy there means nothing at all: it is reachable by answering "makes no
difference" every time.

What has to be measured is the rare class, and what has to be weighed is what
the mistakes cost. The yardstick is the base rate, never zero.
