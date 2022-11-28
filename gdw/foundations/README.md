# Foundations

| Topic | |
|---|---|
| [crisp-dm](crisp-dm/) | six phases, and where the time goes |
| [data-quality](data-quality/) | every repair loses something |
| [scaling-computation](scaling-computation/) | Amdahl against Gustafson |
| [map-reduce](map-reduce/) | why the reducer must be associative |

The first three lectures. Two numbers carry the block: data preparation takes
45 percent of a project against 15 for modelling, and a tenth of serial work
caps the speedup at ten however large the machine.

The recurring shape is that the constraint is somewhere other than where the
attention is. The interesting part of a data science project is the model and
the time goes into the data; the interesting part of a parallel program is
the parallel part and the limit is the serial one.
