# Image layers

Each instruction becomes a layer, and a layer's identifier depends on the
instruction and on everything above it. Change one line and every layer below
it is rebuilt.

Measured over a six-line description by changing each line in turn: a change
at position *p* rebuilds exactly the lines from *p* to the end. Changing the
first line rebuilds all six; changing the last rebuilds one.

## Which is why the order matters

Copying the dependency list and installing it before copying the sources
means a source change rebuilds one layer. Copying the sources first means
every source change reinstalls the dependencies, and the module measures the
difference on the same five instructions in two orders.

## A layer only adds

Deleting a file in a later layer removes it from the view, not from the
image: the bytes stay in the layer below. A large file fetched, used and
deleted across three instructions costs its size in the finished image
forever. Fetch, use and delete belong in one instruction.

Three objects: the description, the image built from it, and the container,
which is an instance of the image with a writable layer on top.
