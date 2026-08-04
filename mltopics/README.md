# Thesis topics: machine learning

Fifty PDFs of thesis offers from several chairs, not a course. Twenty modules
follow the technical themes that recur across them, with the data generated so
that the answer is known before the measurement.

| Block | Modules | What it holds |
|---|---:|---|
| [anomaly-detection](anomaly-detection/) | 6 | four methods and two ways of measuring them |
| [uncertainty](uncertainty/) | 5 | calibration, decomposition, rejection, coverage |
| [automl](automl/) | 5 | the search, and the price of searching |
| [explanation](explanation/) | 4 | four claims and what each leaves out |

The frequency profile of the offers: anomaly detection 222 mentions, time
series 106, Bayesian optimisation 24, meta-learning 22, uncertainty
quantification 12, hyperparameters 12, explainability 12, calibration 12,
outlier exposure 11. Named methods: autoencoder 32, k nearest neighbours,
isolation forest, local outlier factor, Gaussian process, Hyperband.

Several offers are stated as a check on someone else's claim, and three of
those checks are carried out here.

## The claim about deep generative models, in a case with no model

One offer starts from the observation that deep models give unrelated data a
higher likelihood than their own training distribution. Part of that needs no
model at all. For a standard normal in 100 dimensions the log density at the
mode is −91.9 and the mean log density of a sample is −142.0, a gap of
**50.14** against the predicted d/2 = 50. The samples sit on a shell of radius
9.989 against √d = 10, whose thickness of 0.70 does not grow with the
dimension.

Give that model samples from a narrower normal it has never seen and it
assigns them **−104.3** against **−141.8** for its own data. By density the
foreign data are the normal ones. Measured by typicality the foreign sample
stands out at once, at −37.6 against −5.6.

Anyone measuring how much outlier exposure improves calibration has to
subtract this part first, or they are measuring the geometry of high
dimensions.

## The claim about hidden tuning

Another offer calls the evaluation of offline reinforcement learning
fundamentally flawed, because hidden online tuning inflates the reported
numbers. Forty policies that are in truth equally good, all scored on one log,
best one taken: reported **0.535** against a true 0.500, and a second log gives
0.496 back. With 200 policies the inflation grows to 0.040.

The same effect in ordinary hyperparameter search: 500 equally good
configurations give a bias of 0.041, and its size is predictable from the
expected maximum of k standard normals, which matches to within 0.01 at every
k tested.

## What soft labels are worth

The third offer asks whether soft losses help. Two images both labelled deer,
one with 48 of 50 votes and one with 33: after aggregation they are
indistinguishable, and the entropies are 0.28 and 1.19. On the contested
image, a confident model beats a hedging one against the hard label (0.030
against 0.416) and loses against the soft one (1.448 against 0.827). The
ranking of the two models is decided entirely by which label was used.

## Six results from the other modules

**Reconstruction has a blind spot by construction.** An anomaly 56.6 away from
all the data, lying inside the learned subspace, scores **zero**; one 12.0
away but outside scores 144. The method measures the distance to the subspace.

**Without a bottleneck there is no detector.** Separation between normal and
anomalous scores: 1.41 with two components of six, 1.3 × 10⁻¹⁷ with all six.

**Point adjustment turns noise into a result.** A detector flagging 5 % of
points at random goes from an F1 of 0.045 to **0.499** under the protocol
common in time-series anomaly detection.

**Conformal coverage is indifferent to the model.** A model that ignores the
slope entirely gets coverage 0.904 against 0.902 for the correct one, and pays
with a width of 11.41 against 3.32. Coverage says nothing about a model; width
does.

**Two copies of one feature make both look worthless.** Importance 7.98 alone,
**2.00** each when duplicated, and dropping one copy changes the error by
nothing to fifteen digits.

**Bayesian optimisation is for small budgets.** Regret 0.0000016 against 0.054
for random search at 25 evaluations, and 0.0017 against 0.0000 at 120.

## On the verification

Every module is checked against something that shares no code with it: the
normalising term of the isolation forest against its definition, the
reconstruction error against an explicit projection, average precision against
a rectangle sum, the calibration error against a bin-by-bin computation, the
Gaussian process posterior against a direct matrix solve, expected improvement
against Monte Carlo, permutation importance against its closed form for a
linear model, and the interval bounds against sampling.

Ten deliberate faults were planted to see whether the checks catch them. Nine
were caught. The tenth exposed a check that was checking nothing: the identity
total = noise + disagreement cannot fail, because the second part is computed
as the remainder of the first two. Both parts are recomputed independently
now, and the fault is caught.
