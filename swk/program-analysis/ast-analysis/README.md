# AST-based analysis

The cheapest kind of static analysis: match patterns against the syntax tree.

```
java-like tools do this with XPath over the AST; here each rule is a function
```

The lecture's example is a coding standard: find assignment nodes whose target
has a name shorter than three characters. Six rules are implemented in that
spirit.

| Rule | What it finds |
|---|---|
| `short-name` | the lecture's own example |
| `self-assignment` | `x := x`, which cannot change anything |
| `constant-condition` | `if [true]`, where one branch is unreachable |
| `division-by-zero` | a literal zero divisor |
| `never-read` | a variable written somewhere and read nowhere |
| `unreachable` | blocks no execution can reach |

## What the tree can and cannot tell you

It can tell an assignment target from a read, because those are different
positions in the tree. It cannot tell whether a branch is ever taken, because
that depends on values.

`unreachable` is the rule that crosses the line: reachability is a property of
the control flow graph, not of the tree, so it borrows the graph. And even
then it does not fire for `if [false]`, because `flow` is syntactic and puts
edges into both branches regardless. Catching that needs the constant-condition
rule as well, which is why the two usually appear together, and why real tools
run a chain of analyses rather than one.

## Why this is where linters live

PMD, Checkstyle and ESLint are this, scaled up: a rule set, a parser, and a
report. The difference is the number of rules and the quality of the messages,
not the idea. The trade is also visible here: `never-read` is a whole-program
rule, and it is still purely syntactic, so it is fast and it will miss a
variable read through anything indirect. A language with reflection breaks it
outright.
