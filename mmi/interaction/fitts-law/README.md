# Fitts' law

The one quantitative law in interface design: the time to point at something
depends on the distance and the size, and only through their ratio.

    MT = a + b * log2(D / W + 1)

The logarithm is what makes it interesting. Doubling the distance costs the
same as halving the target, and both cost less than proportionally, because
pointing is a sequence of corrections each closing a fixed fraction of the
remaining gap.

| target width at D = 500 | difficulty | predicted time |
|---|---|---|
| 4 | 6.977 bits | 1346 ms |
| 16 | 5.011 bits | 1032 ms |
| 64 | 3.140 bits | 732 ms |
| 256 | 1.562 bits | 480 ms |

## Screen edges are the free win

The cursor cannot overshoot the edge of the screen, so a target against it
behaves as if it extended off-screen. A 4-pixel strip at the edge, 500 away, is
**0.994 bits** instead of 6.977, which makes it easier to hit than a 40-pixel
target in the middle of the screen at 3.755 bits.

That single fact is why the macOS menu bar sits at the very top of the screen
and why Windows taskbar buttons run to the corner.

## The Shannon form and why the original is not used

The 1954 formulation, `log2(2D / W)`, goes negative for targets wider than they
are far: at D = 5 and W = 200 it reports **-4.322 bits**. Adding one inside the
logarithm keeps it at +0.036 and fits the data better at low difficulties. A
negative difficulty is not a statement about pointing but about extrapolating a
fit past its range.

## Fitting

On generated data the least squares fit recovers the parameters exactly
(a = 0.180000, b = 0.120000, R^2 = 1.0000000000). With noise added to each
trial:

| noise sigma | fitted a | fitted b | R^2 |
|---|---|---|---|
| 0.01 | 0.1823 | 0.1198 | 0.9978 |
| 0.05 | 0.1915 | 0.1188 | 0.9460 |
| 0.15 | 0.2144 | 0.1163 | 0.6510 |

`b` stays close while `a` absorbs the noise, which matches how published
studies behave: the slope, and therefore throughput, is the stable quantity and
the intercept is not.

## The effective width correction

The nominal width is what the designer drew; the effective width is what the
user treated it as, computed from the spread of where they actually clicked.
Without it, a participant who trades accuracy for speed looks faster instead of
less accurate, and their throughput is overstated.

## A design question answered by arithmetic

Eight menu items in a column, 24 pixels tall and up to 188 away, against a
radial menu with 60-pixel wedges at a constant distance of 80:

| layout | total | mean per item |
|---|---|---|
| column | 4723 ms | 590 ms |
| radial | **3405 ms** | **426 ms** |

which is the whole argument for pie menus, in numbers rather than in taste.
