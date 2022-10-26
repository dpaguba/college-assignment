# Processing efficiency

The lecture's central table, in relative units:

| | energy per operation | flexibility |
|---|---:|---:|
| ASIC | 1 | 1 |
| FPGA | 30 | 100 |
| DSP | 200 | 500 |
| general purpose | 1000 | 1000 |

A thousandfold difference in efficiency across the same span of flexibility.
The product is roughly constant, within a factor of 3.3, so the trade is a
shape rather than a law, and the programmable middle is about three times
better than a straight interpolation would suggest.

## The memory wall

Processor speed grew about 50 percent a year and memory speed about 7, so the
gap widens exponentially although nothing gets slower. Over twenty years the
ratio grows by a factor of about 900.

Every technique in the hardware chapter answers it, and the embedded answer
differs from the general one. A cache decides at run time and is fast on
average and hard to bound; a scratchpad is allocated by the compiler and has
a known worst case. A real-time system usually takes the second, which is a
case of the whole subject choosing predictability over speed.
