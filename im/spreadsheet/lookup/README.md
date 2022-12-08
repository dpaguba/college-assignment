# Lookup

Two modes, and choosing the wrong one is the quietest error a spreadsheet
makes.

**Exact** (SVERWEIS with FALSCH) is for keys: article number, customer
number. The table need not be sorted, and a missing key is an error rather
than a neighbouring value.

**Approximate** (WAHR, and the default) is for brackets: tax bands, shipping
tiers, grade boundaries. It returns the last entry not above the key, which
requires the table to be sorted ascending.

## What an unsorted table does

The search goes from the top and stops at the first entry above the key. In
an unsorted table the right entry may sit behind that and is never reached.
This module refuses the unsorted table and says so; a spreadsheet says
nothing and returns the value of the row where it stopped.

`unsorted_gives_a_wrong_answer` shows both: the correct answer for 500 € is
Nachnahme, and the row a spreadsheet would stop at gives it by accident here,
which is the worst case, because it means the bug survives the first test.

## The advice

The default in Excel is the approximate mode. For keys, always pass FALSCH.
