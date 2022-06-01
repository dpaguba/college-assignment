# The π-calculus

Lectures 9 and 10. What CCS lacks: names that travel.

| Module | Topic |
|---|---|
| [pi-syntax](pi-syntax/) | free and bound names, α-conversion |
| [pi-reduction](pi-reduction/) | the one reaction rule, and scope extrusion |
| [pi-data](pi-data/) | encoding a list as a process |
| [actors-in-pi](actors-in-pi/) | the actor model as a fragment of the calculus |

In CCS two processes react over a fixed channel name and nothing flows but
the fact of the reaction. Here a name flows, and the receiver can use it as a
channel afterwards. The connection structure therefore changes at run time,
and that is what mobility means.
