# Transactions

What a transaction promises, when a schedule may be called correct, the
protocol that enforces it, what goes wrong when two transactions wait for
each other, and how the state is repaired after a crash.

The centre of the block is a simulated lock manager. On two transactions that
access two items crosswise, 4 of the 6 possible interleavings are not
conflict serialisable, and the lock manager produces neither of them.
