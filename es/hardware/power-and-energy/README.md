# Power and energy

Power is a rate; energy drains the battery. A slower processor can use more
energy for the same work, and the exam's processor is the case where it does.

```
P(f) = 2·10⁻⁶·f³ + 4 milliwatts,  f in megahertz
```

Three million cycles per 100 millisecond period:

| frequency | energy per period |
|---|---:|
| 30 MHz (fills the deadline) | 0.405 mJ |
| 100 MHz (the optimum) | 0.180 mJ |
| 200 MHz (flat out) | 0.300 mJ |

The optimum is where the cubic term and the constant term balance, which is
the cube root of the static power over twice the dynamic coefficient, and for
these numbers that is exactly 100 MHz. The closed form and a numerical search
agree.

With a 3000 mAh battery at 1.2 volts, running at the optimum gives 2000
hours.

## Racing to idle depends on the platform

Finishing early and sleeping beats stretching to the deadline when idling is
free, and loses as soon as idling draws more than about three milliwatts,
because the extra idle time then costs more than the saved switching energy.
The module computes both, and the answer is a property of the hardware rather
than of the algorithm.
