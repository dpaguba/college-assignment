# Data types

The scale of a variable decides which computations mean anything. The first
sheet asks for one example of each type from a sports data set, and the
answer is a classification rather than a calculation: the name of a stadium
is nominal, a league position is ordinal, the number of goals is discrete,
the temperature is continuous, and floodlight on or off is binary.

| Scale | Permitted |
|---|---|
| nominal | mode |
| ordinal | mode, median, quantiles |
| metric | mode, median, quantiles, mean, variance |

The permissions nest, and the module enforces them: asking for the mean of
nominal data raises rather than returning a number. Averaging shirt numbers
is arithmetically possible and answers nothing, which is the only reason a
check like this is worth writing.

The binary case sits in two places at once, since it can be read as a label
or as a count of zero and one, and that double reading is what makes a
proportion both a frequency and a mean.
