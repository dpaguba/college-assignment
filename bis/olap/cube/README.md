# The cube

Twenty-four rows from the exercise sheet: five projects, one row per quarter
and kind of risk, carrying three measures.

- **Dimensions:** Projekt, Quartal, Jahr, Risikoart.
- **Measures:** Risiko-Score, Strategischer Fit, Quartalsbudget.

`build` does not reorganise anything. It keeps the rows and records which
columns are axes and which are content, because that distinction is the whole
of what makes a table a cube.

## Density

Five projects times two quarters times one year times three kinds of risk
gives thirty possible cells. Twenty-four are filled, so the cube is 80 %
dense and six cells are empty: P4 and P5 have no third quarter.

Real cubes are far emptier than this, and the empty cells are not gaps in the
data. They mean the combination did not occur, which is different from zero
and different from unknown. A report that fills them with zero and then takes
an average gets a wrong answer that looks entirely reasonable.
