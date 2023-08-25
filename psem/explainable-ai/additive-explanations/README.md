# SHAP

Lundberg and Lee's construction: the players are the features, and the value
of a coalition is the expected prediction when those features are known and
the rest come from a background distribution.

## The check

For a linear model with an independently drawn background, the contribution of
a feature has a closed form: its weight times the distance of its value from
the background mean. The module computes SHAP by enumeration and compares
against that formula, and they agree exactly. That is a check that shares
nothing with the computation being checked.

## Three properties

Local accuracy: the contributions plus the base value give the prediction.
Missingness: a feature with no effect gets zero. Consistency: if a model
changes so that a feature contributes more in every coalition, its attribution
may not fall.

The paper's theorem is that exactly one additive explanation has all three,
and it is the Shapley value. SHAP is therefore justified by a uniqueness
result and not by how good its pictures look.

## The hidden choice

The background. Change the distribution the absent features are drawn from and
every number changes. It is the same kind of hidden parameter as the
neighbourhood width in the surrogate module, and it is just as rarely
reported.
