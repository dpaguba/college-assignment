# The taxonomy

**Point:** a single value stands out against all others. **Contextual:** a
value stands out only in its context, such as the wrong season. **Collective:**
a sequence stands out although no single value in it does.

And three settings by the labels available: supervised, semi-supervised with
normal examples only, and unsupervised with the assumption that anomalies are
rare.

## Why the kind decides the method

A point method cannot see a contextual anomaly, because it does not know the
context, and cannot see a collective one, because it looks at each value
alone. Whoever skips the classification picks the method at random and then
measures that it does not work.

The survey's own list of what makes the problem hard is worth keeping: the
boundary is not sharp, normal drifts, anomalies are rare and therefore badly
labelled, anyone who wants to avoid detection tries to look normal, and the
base rate makes accuracy meaningless.
