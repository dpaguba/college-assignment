# Concurrency problems

| Topic | |
|---|---|
| [mutual-exclusion](mutual-exclusion/) | four requirements, three failed attempts, Peterson |
| [dining-philosophers](dining-philosophers/) | circular wait, and two ways to break it |
| [readers-writers](readers-writers/) | three policies, and what each gives up |

Three problems that are stated in a sentence and wrong in ways an argument
does not catch. Each is settled here by generating every reachable state: the
mutual exclusion attempts fail at 6 to 26 states, the philosophers deadlock at
two participants, and the reader-writer policies each starve somebody the
table names.

The habit this block builds is the one the rest of the subject depends on.
Running concurrent code proves little, because a run shows one interleaving
out of many and the wrong one may be rare. Enumerating the state space settles
the question, and that is what the process algebras and Petri nets in the
later blocks do at larger scale.
