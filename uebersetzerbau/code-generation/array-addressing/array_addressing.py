"""Array addressing: from indices to a byte address.

Memory is one-dimensional, so a multi-dimensional array is stored by flattening
it, and the compiler generates the arithmetic that undoes the flattening on
every access. Three things decide the formula: the bounds, the element size,
and whether the last index or the first varies fastest.

Non-zero lower bounds, as in Pascal's `array[-5..10]`, make the arithmetic
look worse than it is. The lower bound is a constant, so the whole correction
folds into the base address at compile time and costs nothing at run time.
"""

from __future__ import annotations


class Array:
    """A multi-dimensional array with explicit bounds and a storage order."""

    def __init__(self, bounds, element_size, order="row"):
        """Fix the bounds, the element size and the storage order."""
        self.bounds = [tuple(pair) for pair in bounds]
        self.element_size = element_size
        self.order = order

    def dimensions(self):
        """The extent of each dimension, upper minus lower plus one."""
        return [high - low + 1 for low, high in self.bounds]

    def size(self):
        """Total size in bytes."""
        total = self.element_size
        for extent in self.dimensions():
            total *= extent
        return total

    def linear_index(self, indices):
        """The position of an element counted in elements from the first one.

        Row-major multiplies each index by the product of the extents to its
        right, so the last index moves one element at a time. Column-major does
        the mirror image. Fortran chose one and C chose the other, and every
        interoperability layer between them exists because of that choice.
        """
        self._check(indices)
        extents = self.dimensions()
        offsets = [index - low for index, (low, _) in zip(indices, self.bounds)]

        position = 0
        if self.order == "row":
            for offset, extent in zip(offsets, extents):
                position = position * extent + offset
        else:
            for offset, extent in zip(reversed(offsets), reversed(extents)):
                position = position * extent + offset

        return position

    def offset_in_elements(self, indices, origin_index):
        """How many elements lie between two index tuples.

        This is the form the sheet's reasoning takes: to get from `a[0,0]` to
        `a[3,5]`, skip rows 0 to 2 entirely, three rows of twenty, then five
        more elements in row 3, so 65 elements in total.
        """
        return self.linear_index(indices) - self.linear_index(origin_index)

    def address(self, indices, origin, origin_index=None):
        """The byte address of an element, given the address of another one.

        Anchoring on an arbitrary element rather than on the first one is what
        the exercise asks for and what a compiler actually does: the base
        address it holds is wherever the allocator put the array, and the
        constant correction for the lower bounds is folded in once.
        """
        if origin_index is None:
            origin_index = [low for low, _ in self.bounds]
        return origin + self.offset_in_elements(indices, origin_index) * self.element_size

    def _check(self, indices):
        """Reject indices outside the declared bounds."""
        if len(indices) != len(self.bounds):
            raise IndexError(f"expected {len(self.bounds)} indices, got {len(indices)}")
        for index, (low, high) in zip(indices, self.bounds):
            if not low <= index <= high:
                raise IndexError(f"index {index} outside {low}..{high}")

    def access_code(self, index_names, base_name="base"):
        """The address computation as three-address code.

        Written out to show where the run-time cost of an array access is: one
        multiplication and one addition per dimension beyond the first, plus a
        final scaling by the element size. The lower bounds contribute a single
        constant, which is why a language with them is no slower than one
        without.
        """
        extents = self.dimensions()
        lines = []
        accumulator = None

        for position, name in enumerate(index_names):
            low = self.bounds[position][0]
            if low > 0:
                adjusted = f"{name} - {low}"
            elif low < 0:
                adjusted = f"{name} + {-low}"
            else:
                adjusted = name
            if accumulator is None:
                lines.append(f"t{position} := {adjusted}")
            else:
                lines.append(f"t{position} := {accumulator} * {extents[position]}")
                lines.append(f"t{position} := t{position} + ({adjusted})")
            accumulator = f"t{position}"

        lines.append(f"offset := {accumulator} * {self.element_size}")
        lines.append(f"address := {base_name} + offset")
        return lines
