# IaaS, PaaS, SaaS

Nine layers from the network up to the application. The three models differ
only in where the line is drawn.

| Model | Managed by the customer |
|---|---|
| IaaS | Anwendung, Daten, Laufzeitumgebung, Middleware, Betriebssystem |
| PaaS | Anwendung, Daten |
| SaaS | nothing |

Every layer is managed by somebody, which `split` checks: the two lists
always add up to nine.

## What moves with the line

Convenience and dependency move together. With IaaS the provider owns only
the machine, so changing provider costs effort. With SaaS the provider holds
the data, the processes and the interface, and changing is a project.

Which is why the first question about any cloud service is not what it costs
but where the data sits and how it comes back out.
