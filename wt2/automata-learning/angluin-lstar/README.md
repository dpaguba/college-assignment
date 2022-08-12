# L*

Angluin's algorithm learns an automaton from two kinds of question: does this
word belong to the language, and is this automaton the right one. The second
kind returns a counterexample when the answer is no; the counterexample and
all its prefixes become rows, and the loop repeats.

## What it learns here

| language | states | rounds | membership queries |
|---|---|---|---|
| an even number of a's | 2 | 1 | 5 |
| ends with `ab` | 3 | 2 | 11 |
| a login protocol | 3 | 2 | 22 |

The login protocol is the one that matters for the course: the letters are
log in, log out and view a page, and the learned model has three states, the
third being the error state entered by logging in twice or viewing a page
while logged out.

## Verified against an independent minimisation

40 random automata over two letters and 15 over three were learned and
compared with the target exhaustively up to length 10. Every learned model
agreed, and in every case its state count equalled the number of states of
the minimised target, computed by a separately written partition refinement.
The largest case needed 54 membership queries for 5 states.

## The equivalence oracle is the weak point

Asked to learn "ends with `aab`" with counterexamples searched only up to
length 2, the algorithm returns a one-state automaton and stops, satisfied.
The true model has 4 states, and the one-state model disagrees with the
target as soon as words of length 6 are tried. The result looks like a
finished model and is not one. In practice this oracle is a test suite, and
what it does not test is what the model does not contain.
