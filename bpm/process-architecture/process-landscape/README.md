# The process landscape

The level-one map: the core processes at an abstract level, each pointing at
the more detailed processes below. It is the hardest artefact of the
architecture to get right, because it is the one everybody has to recognise
themselves in.

Three requirements, and `check` tests all three:

- **understandable** for every party involved;
- **complete**, meaning every party finds its own work somewhere in it;
- **compact**, and the rule of thumb puts the ceiling at twenty business
  processes.

The completeness check is the one that fails in practice. A map of twelve
boxes drawn by three managers will be missing the work of the fourth
department, and nobody notices until that department reads it.

## APQC

The Process Classification Framework numbers its entries by depth, and the
notation is the level: `1.0` is a category, `1.1` a process group, `1.1.1` a
process, `1.1.1.1` an activity. `apqc_level` reads the level off the number
and refuses anything that is not digits and dots.

The point of a reference model is not the content but the saved argument: it
standardises where one process ends and the next begins, how the benefit is
quantified, and what things are called. That last one is worth more than it
sounds.

`landscape_example` holds the Wiener Linien map from the lecture, sixteen
processes in three layers.
