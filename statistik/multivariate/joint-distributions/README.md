# Joint distributions

A joint distribution gives a probability to each pair. Summing over one
variable gives the margin of the other, and the margins do not determine the
joint distribution: the product of the margins is one distribution with those
margins, and there are others.

That is the whole reason a joint distribution is needed at all. Two variables
with the same individual behaviour can be related in any number of ways, and
none of that is visible in the margins.

Conditioning fixes a value of one variable and renormalises the other, which
is the same operation as conditioning on an event in the probability block,
applied to a variable instead. The conditional distribution sums to one by
construction, which the tests check, because a conditional distribution that
does not is the usual symptom of dividing by the wrong margin.
