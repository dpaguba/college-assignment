# Fractional factorial designs

Run half the plan by generating one column from the others. With four factors
and D = ABC the plan has 8 runs instead of 16, and the generated column
equals the product of the first three in every row, which the tests verify.

## Aliasing

The defining relation ABCD = I says which effects share a column. The module
computes the alias pairs from the plan itself and confirms that each aliased
pair really has an identical column: no experimental outcome can distinguish
them, whatever the data.

For D = ABC there are 7 alias pairs, among them A with BCD and AB with CD.
The shortest word of the defining relation has length 4, so the resolution is
IV: the main effects are clear of two-factor interactions, and the two-factor
interactions are confounded with each other.

Measured for three generators: D = AB gives resolution III, D = ABC gives IV,
E = ABCD gives V.

## The helicopter

Four parameters, height, wing width, wing length and weight, would need 16
builds; the half fraction needs 8. The design stays orthogonal, so the main
effects are still estimated independently. What is given up is knowing which
of two paired interactions produced an effect.
