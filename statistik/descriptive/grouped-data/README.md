# Grouped data

The second sheet gives heights in six classes of unequal width and asks for a
histogram. The trap is in the widths.

| Class | Count | Width | Height |
|---|---:|---:|---:|
| (140, 160] | 10 | 20 | 0.010 |
| (160, 165] | 8 | 5 | 0.032 |
| (165, 170] | 12 | 5 | 0.048 |
| (170, 175] | 5 | 5 | 0.020 |
| (175, 185] | 14 | 10 | 0.028 |
| (185, 200] | 1 | 15 | 0.0013 |

Plotting the counts would make the tallest bar the class 175 to 185, which
has the most observations and spreads them over ten centimetres. Plotting the
density makes it the class 165 to 170, which has fewer observations packed
into five. The two pictures point at different parts of the data, and only
the second answers the question the histogram is asked.

The area of every bar is the relative frequency, so the total area is one.
That is what makes the histogram comparable with a density and what fixes the
scale of the vertical axis, which the published solution warns about
explicitly.

## What grouping costs

The raw data is gone, so the mean can only be estimated from the class
midpoints, giving 167.7. The median can be located but not computed: it lies
in (165, 170], because that is where the cumulative count passes 25 of 50.
Interpolating inside the class gives a number, and the number is an
assumption about how the observations are spread inside it.
