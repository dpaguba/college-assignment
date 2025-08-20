# Power and energy

Dynamic power in CMOS is `C V^2 f`: linear in frequency, **quadratic** in
voltage. Since a higher frequency needs a higher voltage, scaling both together
makes power roughly cubic in frequency. Halving the frequency with the voltage
leaves an eighth of the power; halving it alone leaves half.

That single fact ended frequency scaling and produced multicore.

## Energy is not power

Energy is power times time, and optimising one does not optimise the other.
Energy alone favours running arbitrarily slowly, delay alone favours running
arbitrarily hot, and the energy-delay product is the usual compromise. At equal
energy it prefers the faster run: 4 W for 1 s and 2 W for 2 s use 4 J each, and
their products are 4 and 8.

## Race to idle, and when it stopped being right

Racing runs at full speed and then idles; crawling stretches the work out. The
cubic term favours crawling, and leakage favours racing, because leakage is
paid per second.

| static power | winner |
|---|---|
| 0 | crawl |
| 30 | race |

The crossover is why the advice changed as leakage grew, and why a modern chip
has deep sleep states rather than only a low-frequency mode.

## Temperature closes the loop

A first-order thermal model makes temperature proportional to power, so every
power saving is a thermal one. The coupling also runs backwards: leakage grows
with temperature, which is a positive feedback loop and the reason thermal
runaway is a real failure mode rather than a theoretical one.
