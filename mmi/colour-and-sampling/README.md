# Colour and discretisation

How a continuous scene becomes numbers, and what is lost at each step.

| Topic | Question |
|---|---|
| [colour-models](colour-models/) | how to name a colour, and which name suits which job |
| [sampling-theorem](sampling-theorem/) | how often to measure, and what happens below that rate |
| [quantisation](quantisation/) | how finely to measure, and where to put the precision |
| [dithering](dithering/) | how to hide the coarseness that is left |

The order is the pipeline order: choose a representation, discretise the
domain, discretise the range, then repair what the last two steps broke.

Gamma appears in three of the four and is the same idea each time: perception
is logarithmic, so the storage should be too.
