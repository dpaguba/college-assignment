# Task types

Seven types, describing the character of a task rather than what it does:

| Type | Person | System | Automatable |
|---|---|---|---|
| send | no | yes | yes |
| receive | no | yes | it waits, the other side decides |
| user | yes | yes | no |
| manual | yes | no | no |
| script | no | yes | yes |
| service | no | yes | yes |
| business rule | no | yes | yes |

Two columns matter and they are not the same column. **Person** says whether
a human does the work. **System** says whether a system sees it happen.

The manual task is the only type where both answers go the wrong way: a
person does it and nothing observes it. For a BPMS the activity does not
exist, which does not stop it from blocking the case.

`make_visible` gives the two ways out of that: implement it as a user task,
so somebody confirms the start and the end in the system, or isolate it and
automate everything around it. The first costs a confirmation from a person
who was not asking for one.
