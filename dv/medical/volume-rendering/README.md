# Volume rendering

A ray through the volume, one sample per slice. Front to back, each sample
contributes its opacity weighted by what the ray still transmits; the
accumulated opacity never exceeds one.

## Checked against the absorption law

With a constant opacity α per sample, the accumulated opacity after n samples
must be 1 − (1 − α)ⁿ. The compositing reproduces that exactly, for α of 0.05,
0.2, 0.5 and 0.9 and for 1, 3, 8 and 20 samples.

Front to back and back to front give the same image to 1e-9 at every pixel,
which they must: the two are algebraically the same operation, differing in
what has to be carried along.

## The transfer function is the picture

The same volume with a transfer function for dense material gives an opacity
of 0.99; one that shows only the weak material gives 0.51. Nothing about the
data changed. Choosing the transfer function is choosing what the image is
of, which is why the lecture treats it as part of the analysis rather than a
display setting.

Maximum intensity projection takes the largest value along the ray instead of
compositing. It is independent of the order, which the module checks by
reversing the ray, and it discards all depth information in exchange.

Stopping the ray once the opacity passes 0.99 changes no pixel by more than
0.01, so early termination is a saving rather than an approximation worth
worrying about.
