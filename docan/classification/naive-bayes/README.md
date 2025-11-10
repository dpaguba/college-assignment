# Naive Bayes

The class prior is its share of the documents. The class-conditional
probability of a term is its share of all term occurrences in the class,
smoothed as the slide gives it:

```
P(wt|Ki) = (1 + Σ ft) / (|V| + Σ Σ fs)
```

Checked against exact fractions over 200 random problems, both the estimates
and the decision.

## What the smoothing prevents

Without it, a term that never occurs in a class has probability zero. A single
such word in a document then multiplies the whole class to zero, no matter how
well everything else fits. One unseen word would veto the class, and in a
vocabulary of thousands there is always an unseen word.

## Why the log domain is not a nicety

Two thousand terms at a thousandth each:

| | |
|---|---|
| direct product | **0.0** |
| in the log domain | −13 815.5 |
| smallest positive double | 5 × 10⁻³²⁴ |

The product is far below anything a double can hold, so comparing two classes
becomes comparing two zeros. In the log domain it is an ordinary number.

## What "naive" names

The terms are treated as independent given the class. For language that is
false: "New" is followed by "York" far more often than chance. The method
therefore counts shared information several times and produces probabilities
that are far too confident. The decision usually survives anyway, because only
the order of the classes matters and not the height of the values, which is
also why the confidence of a naive Bayes classifier should not be reported as
one.
