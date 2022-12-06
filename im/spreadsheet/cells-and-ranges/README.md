# Addresses and ranges

An address is a column, a row, and up to two dollar signs. The column letters
are the interesting part: they are not an ordinary place-value system,
because there is no zero. After Z comes AA, not BA, which is why the
conversion subtracts one before each division.

`column_number` and `column_letters` are checked against each other for the
first eight hundred columns.

## Named ranges

The exercise asks for five: the VAT rate, the two net price ranges and the
two gross price ranges.

A name behaves like an absolute reference and applies across the whole
workbook. That is both its advantage and its trap. It makes the formula
readable, `=C6*(1+Umsatzsteuersatz)` instead of `=C6*(1+$D$22)`, and it does
not tell anybody when somebody later moves the range it points at.
