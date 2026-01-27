# Windows over a series

Three kinds of anomaly that get treated as one: a point that stands out in any
context, an ordinary value in the wrong place, and ordinary values in an
unusual sequence.

## The window length is a statement, not a setting

A level shift the size of the noise, over 40 runs:

| window | found the shift |
|---:|---:|
| 3 | **37.5 %** |
| 60 | **90 %** |

A shift consists of unremarkable values. A short window sees nothing special
in any of them; a window that spans the boundary sees two levels in one view.
The window length therefore says how long an anomaly is allowed to be, and
that is a decision about the phenomenon rather than about the algorithm.

## The value that is ordinary and still wrong

A series with a period of 24, amplitude 3, and the value **+3.0** planted at a
trough:

| detector | score | flagged at 2σ |
|---|---:|---|
| height only | 1.40 | no |
| after removing the season | **14.62** | yes |

The value occurs at every peak, so it is entirely ordinary; its position is
not. A detector that only measures height cannot say so, and no threshold on
that detector will fix it.

## What a window gives back and what it cannot

It restores the ordering within its own length. It cannot see a trend across
the whole series, a period that does not fit inside it, or any dependence
across its boundary. Every window method therefore begins with a decision
about the time scale, usually an unspoken one.
