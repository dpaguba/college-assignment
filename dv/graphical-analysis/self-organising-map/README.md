# Self-organising map

A grid of weight vectors that is pulled towards the data. Each step finds the
best matching unit, then moves it and its neighbours on the grid towards the
sample. Learning rate and neighbourhood radius both decay, so the map is first
arranged roughly and then refined.

Training lowers the quantisation error, which the module measures before and
after.

## The topology is the point

Trained on data spread along a line, a one-by-six map ends with its weights
in monotone order along the chain: neighbours on the map are neighbours in
the data. That holds across five different seeds. This is what separates the
map from plain vector quantisation, which would place the same number of
prototypes with no relation between them, and it is why a two-dimensional map
can be drawn as a picture of a higher-dimensional data set.
