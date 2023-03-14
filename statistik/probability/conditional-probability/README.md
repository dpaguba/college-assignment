# Conditional probability

Conditioning restricts the space to the given event and renormalises, so the
formula is a definition. What follows is the law of total probability, which
decomposes an event along a partition, and Bayes' rule, which reverses the
direction of the conditioning.

The seventh sheet works it through:

```
P(practice passed | exam passed) = 0.8
P(practice passed | exam failed) = 0.2
P(exam passed) = 0.7

P(practice passed) = 0.8 · 0.7 + 0.2 · 0.3 = 0.62
P(exam failed | practice passed) = 0.2 · 0.3 / 0.62 = 0.097
```

Both are reproduced. The published solution notes its own typing errors in
these two numbers, which is a reminder that a printed answer is not
automatically the right one, and the reason every published value here is
recomputed rather than copied.

## The reversal is the point

The two conditional probabilities are different questions and are routinely
confused. A test that is right 99 percent of the time on a condition that
affects 1 percent of people gives, on a positive result, a probability of
about 17 percent that the person has it. The module includes that
calculation, because the number is the argument.
