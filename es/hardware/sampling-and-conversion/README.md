# Sampling and conversion

The exam asks about the boundary case: a 1000 Hz signal sampled every
millisecond. That is 1000 samples per second against a Nyquist rate of 2000,
so the answer is no, and it stays no at exactly 2000: a sine sampled at
exactly twice its frequency can be caught at its zero crossings and vanish.

Under-sampling does not lose the signal quietly. A 1200 Hz signal sampled at
1000 Hz appears as a 200 Hz signal that fits the samples exactly, and nothing
in the samples says which of the two was there. That is why an anti-aliasing
filter comes before the converter and not after it.

## The two converters

| | comparators | steps |
|---|---:|---:|
| flash, 4 bits | 15 | 1 |
| successive approximation, 4 bits | 1 | 4 |

The comparison the exam asks for, in two numbers. The flash converter spends
hardware exponential in the resolution and answers in one step; the
successive approximation converter spends one comparator and a step per bit,
which is a binary search over the range. Every bit added doubles the hardware
of the first and adds one step to the second.
