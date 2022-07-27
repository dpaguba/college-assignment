# Metrics report

One report over a real code base, joining the four measures.

```
python3 metrics_report.py ../../dap2
```

The lecture's own motivation for this whole topic is a question: would it not
be good if coding standards and metrics could be checked automatically? This
is that check, pointed at the Python in this repository.

## What it adds

Extracting the class models LCOM needs from real source. Fields are the
`self.x` attributes a class touches, methods are its functions, and an access
is a method mentioning a field. That is what turns LCOM from an exercise on
paper into something that can be run over a directory.

## The output on dap2

```
cohesion, worst classes by LCOM
  0.76  LCOM4=2  skip_list.py:SkipList
  0.72  LCOM4=7  b_tree.py:BTree
  0.70  LCOM4=3  trie.py:Trie

coupling, most depended upon
  Ca= 2 Ce= 0 I=0.00  union_find
  dependency cycles: none

coding standard
   53  missing-docstring
   10  long-function
    9  high-complexity
```

## How to read it, and how not to

Every number here is a **question**, not a verdict. `BTree` scoring 7
components is not a defect: a B-tree node genuinely has several independent
concerns, and splitting it would make the code worse. The value of the report
is that it points at the three or four places worth looking at, out of a
hundred files.

The moment any of these numbers becomes a target in itself, it stops measuring
anything, which is the same warning the
[monitoring](../../estimation/monitoring/) module makes formal as Goodhart's
law.
