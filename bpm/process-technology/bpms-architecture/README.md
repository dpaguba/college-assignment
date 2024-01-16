# The architecture of a BPMS

Five components:

| Component | Does |
|---|---|
| process modelling tool | capture models and annotate them for execution |
| execution engine | create instances, move tokens, hand out work |
| worklist handler | show each role the tasks waiting for it |
| administration and monitoring | watch running instances, intervene, report |
| external services | everything the process cannot do itself |

The engine is the centre because it holds the state of every instance.
Everything else writes into it or reads out of it; without it there are
pictures of processes and no processes.

External services are the ones the exercise asks for three of: a payment
provider, a credit check, sending mail, a document archive, the accounting
system.

## What it is not

Not an ERP: the master data lives elsewhere. Not the services: it
orchestrates, it does not compute. And not a drawing tool, which is the
confusion that costs the most, because a model that was only drawn does not
run anywhere.
