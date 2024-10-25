# ERP

The problem first: large organisations run many specific systems, each with
its own data and no automatic exchange. Managers cannot assemble an accurate
picture without collecting figures by hand. The answer is one integrated
system with one database, where a posting takes effect in every module at
once.

## Make or buy

`make_or_buy` puts the two options side by side. Standard software costs a
licence per user plus a one-off implementation project; a bespoke system
costs a fixed amount that does not grow with the number of users. The
break-even follows: below a certain number of users the bespoke system is
cheaper, above it the licence.

At 1000 € per user, 100 000 € for the project and 300 000 € for building, the
break-even is 200 users.

The sum leaves out operations, and that omission favours the bespoke option,
which is exactly the option operations hits hardest.

## Customising is not programming

Customising adapts the standard system through settings: charts of accounts,
document types, approval limits. The source code is untouched, so the
adaptation survives the next update. Extending the source code means paying
again at every update, for ever.

The rule of thumb the course gives: adapt the process to the software first,
and the software to the process only where the process is genuinely the
organisation's own.
