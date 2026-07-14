# Mini-Compiler Explorer

Single HTML file, no dependencies. Open it by double-clicking; works offline.

Covers the whole lecture sequence of Übersetzerbau (SoSe 2025 / SoSe 2026):

| Phase in the demo | Topic |
|---|---|
| 1 Scanner | `02-Scanning.pdf` |
| 2 Parser | `03-Parsing.pdf`, `04-Parsing - TopDown.pdf` |
| 3 AST | `06-AST.pdf` |
| 4 Symbols & Types | `07-Symbol.pdf`, `08-TypeChecking.pdf` |
| 5 Code | `09-Codeerzeugung.pdf` |
| 6 Execute | stack machine that runs the generated code |

The `SCAN → PARSE → WEED → CODE → RUN` strip at the bottom left is the pipeline
from slide `09-Codeerzeugung.pdf`; a phase turns red when it reports an error.

Eight sample programs are built in, including three that fail on purpose, one per
phase, so the difference between a lexical, a syntactic and a semantic error is visible.

Language: `let`, assignment, `print`, `if`/`else`, `while`, `int` and `bool`,
arithmetic, comparison, block scope.
