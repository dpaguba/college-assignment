# Deployment strategies

| strategy | downtime | peak instances (of 4) | first exposure |
|---|---|---|---|
| recreate | 1 step | 4 | everyone |
| blue green | none | 8 | everyone |
| rolling | none | 5 | a quarter |
| canary | none | 5 | a fifth |

Recreate is the cheapest in machines and the only one with downtime. Blue
green has no downtime and needs the whole fleet twice over. Rolling needs one
spare and exposes users gradually as instances are replaced. Canary sends a
small share of traffic to one new instance and waits before continuing.

## Rolling back

Blue green and canary roll back in one step: the old version is still
running and the switch goes back. A rolling update has to reverse every
instance it already replaced, which the module counts as four steps against
one.

That is the argument for blue green despite the doubled capacity: the cost is
paid in machines during the change, and what is bought is a rollback that
takes a second rather than a procedure.

All four need the same things: the two versions must run side by side, the
database schema must fit both for a while, a health check must say when an
instance is ready, and the way back must have been practised.
