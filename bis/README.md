# Betriebliche Informationssysteme

Twenty-six modules in five blocks, following the lecture: how data is
modelled, how it is analysed once it is in a cube, what the systems around
it are called, how projects and cloud decisions are made, and what machine
learning adds.

| Block | Modules | What it holds |
|---|---:|---|
| [data-modelling](data-modelling/) | 6 | ER with (min,max), specialisation, mapping to tables, data quality |
| [olap](olap/) | 6 | the cube and the six operations on it |
| [enterprise-systems](enterprise-systems/) | 6 | the system pyramid, integration, ERP, CRM, analytics |
| [project-and-cloud](project-and-cloud/) | 6 | project portfolio, risk, cloud models, outsourcing |
| [machine-learning](machine-learning/) | 2 | the three kinds of learning, and what bad labels do |

## The data

Three of the modules work on a real table rather than an invented one. The
exercise sheet ships `EiWI_BIS_Z5_Tabelle.csv`: five projects, each with one
row per quarter and kind of risk, carrying a risk score, a strategic fit and
a quarterly budget. Twenty-four rows, which is exactly enough to be a cube
and small enough to check every figure by hand.

It also carries two defects, and finding them is the point:

**The strategic fit contradicts itself.** It is a property of the project, so
inside one project it must not depend on the kind of risk. For four projects
it does not. P5 IoT Produkt has 8 in the rows for technical and
organisational risk and 9 in the row for market risk. Which one is right the
data does not say; that they disagree, it does.

**The budget is not additive over the kind of risk.** It belongs to the
project quarter and is repeated in all three rows of it. Summing the column
gives 8730 T€ where the actual total is 2910 T€, a factor of three. This is
the ordinary way a report ends up wrong: nothing is missing, nothing is
mistyped, and the number is still three times too large.

## Verification

Every OLAP operation is checked against a plain scan over the rows: roll-up
against grouping by hand, slice and dice against filtering, drill-through
against recomputing the figure from its rows. Drill-down is checked against
roll-up on every axis, and the sums agree. Rotation is checked by applying it
twice on all twelve ordered pairs of dimensions, which must return the
original table.
