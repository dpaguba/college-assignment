# Quantiles and boxplots

The course defines the quartiles as the medians of the two halves of the
sorted sample. On the exam data that gives 2 and 3, which is what the
published solution prints.

That definition is one of several. Statistical software often interpolates
and reports other numbers on the same data, so the convention has to be
stated with the result. The module implements the course's version, and the
tests check it against the published values rather than against another
implementation.

## The five numbers

```
minimum  1
lower    2
median   2
upper    3
maximum  4
```

The box holds the middle half and the line inside it is the median, so a box
plot shows where the data is and how it is spread without assuming any shape.
The second sheet uses two of them side by side to compare the ages of two
national squads, and the comparison is exactly what the plot is for: the men
have the stronger outliers, the women's middle half is wider.

## The empirical distribution function

A staircase rising by one over n at every observation. It contains everything
the sample knows, and every quantile is read off it, which is why the module
computes the quantiles from it rather than the other way round.
