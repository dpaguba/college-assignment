# State charts

The exam's cookie machine: a power button, a size button with two settings
and a crunchiness button with three, and the crunchiness has to survive being
switched off while the size does not.

A flat automaton needs twelve states for that, plus something to remember the
setting. The chart needs three small machines: the two settings are parallel
states inside the machine and the crunchiness carries a history marker.

```
machine ──┬── off
          └── on ──┬── size:        big ⇄ small
                   └── crunchiness: very crunchy → soft → crunchy → (H)
```

The whole behaviour of the exam question is reproduced: the default is big
and very crunchy, the crunchiness cycles in that order, and after a power
cycle the crunchiness is restored while the size returns to big. The history
marker is one symbol and it replaces a duplicate of the entire settings
machine.

That is the argument for the notation. Hierarchy removes the repetition of
transitions that apply to a whole group, parallel states remove the product
of independent components, and history removes the copies that differ only in
what they remember.
