# Event scheduling

Time is data. The engine holds a calendar, takes the earliest event, moves
the clock to it and lets it schedule more. Nothing else advances the clock,
so a simulated hour in which nothing happens costs no computation at all.

An event that schedules another inherits its handler unless it names one,
which is how a recurring event describes itself once. Simultaneous events
keep their insertion order, because the alternative is a result that depends
on the internals of the queue.

The horizon stops the run, and it belongs in the engine rather than in the
model: a model that decides when to stop cannot be reused for a longer study.
