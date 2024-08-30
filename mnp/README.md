# Modellierung nebenläufiger Prozesse

Thirteen modules in four blocks, ordered so that each one answers a question
the previous one could only raise.

| Block | |
|---|---|
| [concurrency-problems](concurrency-problems/) | mutual exclusion, philosophers, readers and writers |
| [actor-model](actor-model/) | mailboxes, ordering, supervision |
| [process-algebra](process-algebra/) | CCS, bisimulation, the pi-calculus |
| [petri-nets](petri-nets/) | structure, reachability, properties, workflow nets |

The Akka project from the practical is in [assignment](assignment/).

## The through-line

Concurrent code cannot be validated by running it, because a run exhibits one
interleaving and the broken one may be rare. Every block here answers instead
by enumerating: 26 states settle Peterson's algorithm, 14 markings settle
three dining philosophers, and 4 markings settle the exercise-sheet net
completely.

What changes between blocks is what gets enumerated. The first block
enumerates program counters and shared variables. The third enumerates the
transitions a syntax derives. The fourth enumerates markings, and adds the one
technique that avoids enumeration altogether.

## Numbers worth keeping

| | |
|---|---|
| Peterson, states explored | 26 |
| single flag / two flags / strict alternation | fails at 24 / 12 / 6 states |
| philosophers, naive strategy | deadlocks from 2 participants up |
| philosophers eating at once, out of 5 | 2 |
| three philosophers as a net | 14 markings, 1 deadlock |
| exercise-sheet net | 4 markings, 4 edges, 1 deadlock |
| buffer of capacity 3 | 3 consecutive `in` |
| `a.(b+c)` against `a.b+a.c` | same traces, not bisimilar |
| exactly-once after 2 failures | 1 delivery, at the cost of receiver state |

## Three results worth arguing about

**The philosophers' real limit is throughput.** Deadlock is what the problem
is famous for and it is the easy part: order the forks, or seat one fewer
philosopher. The ceiling that survives every fix is floor(n/2) eating at once,
so five philosophers use two seats. A solution can be entirely correct and
still leave more than half the table idle.

**Same traces is the wrong test.** `a.(b.0 + c.0)` and `a.b.0 + a.c.0` have
identical trace sets and behave differently in the way a user notices: after
the `a`, one still offers a choice and the other has already made it.
Everything that depends on what remains available after a partial run needs
bisimulation, and deadlock freedom is one of those things.

**AND-split with XOR-join is unsound, and it looks fine.** The join fires when
the first branch arrives, the case completes, and the second branch's token
stays behind. The net catches it as a proper-completion failure at 5
markings. A BPMN diagram of it draws cleanly and reviews cleanly, which is the
argument for giving the diagram a formal semantics rather than trusting the
picture.

## Two formalisms, one answer

The dining philosophers are settled twice: by exhaustive interleaving in the
first block and by reachability in the fourth. Both find the deadlock at three
participants. The net additionally names the state, `left0 left1 left2`, every
philosopher holding one fork, which is the difference between knowing a system
can fail and knowing how.
