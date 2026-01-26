# Reconstruction

Learn to rebuild the normal data through a bottleneck, then score a point by
how badly the rebuild fails. The thesis offer states the reasoning openly: the
model fails on an anomaly because it was not trained on one.

## The bottleneck is the detector

| model | separation between normal and anomalous scores |
|---|---:|
| two components of six | **1.41** |
| six components of six | **1.3 × 10⁻¹⁷** |

At full rank the reconstruction is exact for every point, including the
anomalous ones, and the score separates nothing. An autoencoder without a
narrowing is not a weak detector, it is not a detector.

## What it cannot see, by construction

An anomaly that happens to lie inside the learned subspace is rebuilt
perfectly:

| point | distance from the data | score |
|---|---:|---:|
| inside the subspace | **56.6** | **0.0** |
| outside it | 12.0 | 144.0 |

The method measures the distance to the subspace, not the distance to the
data, and the two get confused routinely. Using it means assuming that being
anomalous leads out of the subspace.

## Where the heuristic runs out

A model with enough capacity learns to rebuild the unseen as well; a model
with too little fails on the normal data too. The usable range lies between,
and where it lies can only be measured.
