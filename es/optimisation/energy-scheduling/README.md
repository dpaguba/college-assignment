# Energy aware scheduling

The rule is that a task with slack should run slower, because the switching
energy grows with the square of the frequency for a fixed amount of work. The
module confirms that half: stretching the exam's task from 200 MHz to 30 MHz
cuts the switching energy by a factor of 44.

And the rule is wrong on this processor. The static draw of four milliwatts
is paid for the whole execution, so the totals are:

| strategy | frequency | energy per period |
|---|---:|---:|
| fill the deadline | 30 MHz | 0.405 mJ |
| the optimum | 100 MHz | 0.180 mJ |
| flat out | 200 MHz | 0.300 mJ |

Filling the slack is the worst of the three, and worse than doing nothing
clever at all. The optimum is interior, at the point where the cubic and the
constant terms balance, and finding it needs the static power to be part of
the model.

That is the difference between the textbook rule and the exam's question. The
rule is about dynamic energy; the question is about a battery.
