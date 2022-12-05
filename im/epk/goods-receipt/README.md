# Goods receipt

The second exercise of tutorial one. The point of the exercise is in part c:
the packaging check runs at the same time as the quantity check and is done
by a different employee. Modelling them one after the other describes a
process the company does not have.

The order is: check whether the material was ordered at all; if it was, check
quantity against the delivery note and packaging in parallel; if both pass,
sign for the driver and start the quality check, again in parallel;
otherwise refuse acceptance. Defective goods are claimed with the supplier,
faultless goods are stored.

## The short circuit

`outcomes` enumerates all eight combinations of the three checks. Four of
them are decided by the first: if the material was not ordered, acceptance is
refused without anybody looking at quantity or packaging. In the model that
is an exclusive split placed before the parallel one, and getting the order
wrong means modelling two checks that in half the cases never happen.

Exactly one of the eight combinations leads to acceptance.
