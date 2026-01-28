# Density is not belonging

The thesis offer starts from the observation that deep generative models
assign higher likelihood to unrelated samples than to their own training
distribution. Part of that is not a model failure at all. It happens with a
perfectly known Gaussian.

## The mode and the samples

For a standard normal in 100 dimensions:

| | |
|---|---:|
| log density at the mode | −91.89 |
| mean log density of a sample | −142.03 |
| gap | **50.14** |
| predicted gap, d/2 | 50 |
| mean radius of a sample | 9.989 |
| √d | 10 |
| spread of the radius | 0.700 |

The density is highest at the origin and almost no point is ever there. The
samples sit on a shell of radius √d whose thickness does not grow with the
dimension. The gap in log density is exactly d/2, and it is measured at 1.0,
4.96, 25.01 and 100.28 for d = 2, 10, 50 and 200.

## The foreign sample looks more likely

A model for the standard normal, given its own samples and samples from a
narrower normal it has never seen:

| sample | mean log density | typicality |
|---|---:|---:|
| its own | −141.77 | **−5.6** |
| the narrow foreign one | **−104.33** | −37.6 |

By density alone the foreign data are the normal ones. The error is not in the
model; it is in the assumption that high density means belonging. Measured by
typicality, the distance of the log density from its expected value, the
foreign sample stands out at once.

## What this means for the experiment

Anyone measuring how much outlier exposure improves calibration has to
subtract this part first. Otherwise the measurement is of the geometry of high
dimensions and not of the method.
