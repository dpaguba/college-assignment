# Public Function

A **Sub** does something and returns nothing; it sits behind a button. A
**Function** returns a value and can therefore be called from a cell. Only a
Function appears among the user-defined functions in the assistant. In VBA
the return value is assigned to the function's own name.

## ByRef is the default

VBA passes arguments by reference unless `ByVal` says otherwise, which is the
opposite of what most languages one learns alongside it do. A function that
changes an argument changes the caller's variable, and that explains a whole
class of bugs that surface far away from the function.

## Why a worksheet function must not write

A function called from a cell may not change the sheet. It is called on every
recalculation, and writing during a recalculation would trigger the next one.
Excel therefore rejects such writes silently: the cell shows an error value
and the sheet is unchanged. When a change to the sheet is what is wanted, the
right tool is a Sub behind a button.
