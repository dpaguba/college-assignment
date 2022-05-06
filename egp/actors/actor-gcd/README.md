# Euclid with actors

Exercise 3 of sheet 3. The actor receives two numbers and a reply address; if
the second is zero it sends the first back, otherwise it sends itself the
second and the remainder.

There is no loop, and that is the point. An actor handles one message and is
then ready again; a loop inside it would block every other message for the
duration of the computation. The chain of messages to itself gives up control
between every two steps.

The price is visible: one message per step, and the state of the computation
has to travel in the message, because the actor should not hold anything
between messages that does not belong to it.

Checked against the library's `gcd` for all 625 pairs up to 24.

## Division against subtraction

Euclid's original subtracts rather than divides. Both give the same answer;
the message count does not. For 1000 and 3, subtraction takes 336 messages
and division takes 3.
