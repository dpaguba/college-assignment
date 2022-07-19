# A/B testing

A metric tells you what happened; an experiment tells you whether your change
caused it. Everything here is the two-proportion test, because the exercise's
metric is a conversion rate.

## Sample size comes first

| To detect | Users per group |
|---|---|
| +20% on a 10% baseline | 3,841 |
| +10% | 14,751 |
| +5% | 57,763 |

Halving the effect roughly **quadruples** the sample, which is the arithmetic
behind most abandoned experiments. Deciding the smallest effect worth
detecting in advance is what fixes how long to run, before any data can tempt
anyone to stop early.

## Reading the result

```
control 10.000%, variant 11.200%, lift +12.0%, z = 2.76, p = 0.0058, significant
```

The p-value answers one narrow question: if the change did nothing, how often
would chance alone produce a difference this large. It is **not** the
probability that the change works, and reading it that way is the most common
mistake made with these numbers.

The confidence interval is the more useful output. "Conversion rose to 11.2%"
and "rose to somewhere between 10.6% and 11.8%" are different claims, and only
the second is supported.

## Peeking, simulated

Both groups given the **same** true rate, so every significant result is a
false positive:

| How the test is read | False positives |
|---|---|
| tested once at the end | 5.0% |
| peeked at 10 times, stopped at the first significant look | 17.4% |

The nominal rate is 5%. Looking repeatedly and stopping when the answer looks
good turns a one-in-twenty error rate into better than one in six, and nothing
in the output of the test says so. It is the most expensive habit in practical
A/B testing, and it costs nothing to demonstrate: those numbers come out of the
same simulation, from this module, in a few seconds.

Sequential testing methods exist for exactly this case, and the fair summary
is: either fix the sample size in advance, or use a method designed for
peeking. Not both, and not neither.
