# Informationsmanagement

Twenty-four modules in five blocks, following the fourteen tutorials of the
course. There are no lecture slides in the folder: the tutorials are the
whole record, and they run from process modelling through databases into
spreadsheets and VBA.

| Block | Modules | What it holds |
|---|---:|---|
| [epk](epk/) | 5 | the event-driven process chain and its two exercises |
| [data-model](data-model/) | 3 | the furniture chain's schema and its mapping to tables |
| [sql](sql/) | 6 | DDL, DML and the query exercises, against sqlite3 |
| [spreadsheet](spreadsheet/) | 6 | addresses, references, formulas, lookup, planning |
| [vba](vba/) | 4 | control flow, loops, arrays, user-defined functions |

## The database

The example runs through the whole course: the furniture chain "Fröhliche
Einrichtung", with customers, articles, warehouses, sellers, receipts and a
"customer recruits customer" relation. The schema comes from tutorial five
and the shape of the data from tutorial six.

The full population lived on the course's own SQL platform and is not in the
folder, and the exercises reference rows the sheets never show: receipt 23,
customers 10 and 11, article 6, a warehouse in Dortmund Wambel, turnover for
2007. The database here is therefore reconstructed: the schema is exactly the
one described, and the population is extended so that every exercise has an
answer. Each query module says so.

Every query is checked twice: once by sqlite3 and once by counting the same
tuples in Python. The two paths agree on all of them.

## Three findings

**The mapping rules and the tutorial's own tables disagree twice.** By the
rules, "customer recruits customer" needs no table of its own, because the
recruited side has at most one recruiter, so the foreign key belongs in the
customer table. Tutorial six creates a separate table anyway, which is the
better choice for a different reason: it keeps a mostly empty column out of
the customer table and leaves room for an attribute later. And `betreut`
would get a three-column key as a ternary relation, but in the data the pair
of receipt and article already determines the seller, so it is really a
binary relation with the seller as an attribute.

**The jubilee gift rules of the Excel exercise partition the cases exactly**,
if the two mentions of purchases mean the same number: "since 2014 and at
most five purchases" is the exact negation of "a customer for more than four
years or more than five purchases". Checked over 132 combinations, no
customer falls into both and none into neither. Read as two different
numbers, lifetime purchases against this year's, the partition breaks and a
customer with eight purchases in total and two this year gets nothing. The
sheet does not say which reading it means.

**Ranking a production programme by absolute contribution margin costs a
third of the profit.** With the bottleneck at 500 kg the correct ranking, by
margin per bottleneck unit, yields 5760 €; ranking by the absolute margin
yields 3840 €. The correct figure was verified against a bounded-knapsack
dynamic programme over the same capacity, which reaches the same 5760 €.

## A note on the material

The PDF of tutorial five does not render: the font carries no glyphs and the
page shows rows of boxes. The text layer is intact, and `pdfminer` extracts
it in full. That was worth finding out.
