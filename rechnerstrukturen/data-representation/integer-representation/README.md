# Integer representations

Four ways to write a signed integer, agreeing on non-negative numbers and
disagreeing on everything else. That is why the exercise asks for the same
value in all of them.

`(101)` in eight bits:

| representation | pattern |
|---|---|
| sign and magnitude | `01100101` |
| ones' complement | `01100101` |
| two's complement | `01100101` |
| excess by 127 | `11100100` |

The same pattern read back differs as soon as the top bit is set. `11011010` is
**-90**, **-37**, **-38** and **91** in the four representations.

## Why two's complement won

| representation | zeros | range in 8 bits | addition |
|---|---|---|---|
| sign and magnitude | 2 | -127..127 | inspect the signs first |
| ones' complement | 2 | -127..127 | end-around carry |
| two's complement | **1** | -128..127 | **the unsigned adder, carry discarded** |
| excess by bias | 1 | -bias..255-bias | subtract the bias |

Verified exhaustively: over all 5-bit operand pairs, two's complement addition
gives the mathematical sum with no case distinction and no spurious overflow.
The two zeros of the other two representations are not cosmetic either, since
every comparison against zero needs two tests.

The asymmetric range is the price: `-128` has no positive counterpart, so
negating it overflows.
