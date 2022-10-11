# Little's law

WIP = λ · CT. Solve for any of the three and the other two decide it.

The law holds for any stable system, whatever the distributions are. That is
what makes it useful: two of the three quantities are usually easy to count,
and the third is the one nobody measures.

## The restaurant

1200 guests a day, open from 10 to 22. Six hours of peak (12 to 15 and 18 to
21) take 900 guests with 90 present on average; the other six hours take 300
with 30 present.

| | Arrival rate | Present | Stay |
|---|---:|---:|---:|
| Peak | 150 /h | 90 | 36 min |
| Off peak | 50 /h | 30 | 36 min |

Both windows give the same 36 minutes. The busy hours differ in how many
guests come, not in how long one of them stays, which is not what the word
"peak" suggests and falls straight out of the law.

The third part of the exercise asks what to do when the 110 seats are
reached and demand still grows. Little's law leaves exactly one lever: the
seats are fixed and the arrivals are given, so the stay has to get shorter.
At 36 minutes the room supports 183 arrivals an hour; at 30 minutes it
supports 220.

`check_by_simulation` builds an arrival stream with exponential gaps, gives
every case the same fixed stay, and measures the time-weighted average
number inside. It lands on λ · CT.
