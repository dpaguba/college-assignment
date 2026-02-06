# Anomaly detection

| Module | Topic |
|---|---|
| [density-and-distance](density-and-distance/) | global against local density |
| [isolation-forest](isolation-forest/) | depth instead of distance |
| [reconstruction](reconstruction/) | the bottleneck, and its blind spot |
| [time-series-windows](time-series-windows/) | what the window length decides |
| [typicality-vs-density](typicality-vs-density/) | why high density is not belonging |
| [detection-metrics](detection-metrics/) | measuring when the case is rare |

The dominant theme of the folder, with 222 mentions across the topic offers.
Four methods and two ways of measuring them, and the two most useful results
are both negative.

Reconstruction scores an anomaly 56.6 away from the data at **zero**, because
it measures the distance to the subspace rather than to the data. And the
common point-adjustment protocol takes a detector that flags 5 % of points at
random from an F1 of 0.045 to **0.499**.
