# Full factorial designs

The 2^k design: every factor at two levels, every combination run. The runs
are listed in Yates order, the first column alternating every row, the second
every two rows.

Every column is balanced and every pair of columns is orthogonal, checked for
k from 2 to 5. Orthogonality is what allows each effect to be estimated
without regard to the others.

## Effects

The main effect of a factor is the mean response at its high level minus the
mean at its low level. An interaction is the same computation on the product
column. The estimates are compared with a least-squares fit through numpy:
the regression coefficients are exactly half the effects, which is the
relation the lecture writes down as the regression function.

## The exercise

Operation A or B, diagnosis X or Y, clinic 1 or 2: three factors, eight runs,
all eight combinations listed. If the complication rate differs between the
two clinics at the same operation and diagnosis, the cause lies outside the
three factors, in what the plan did not control: case mix, surgeon
experience, aftercare.

Reducing a 2^k plan all the way leaves fewer runs than there are effects, and
the main effects then merge with interactions and cannot be separated.
