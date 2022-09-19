# Docker and continuous practices

Layers and their cache, the pipeline and the cost of the wrong stage order,
and the four ways to put a new version into service.

Two measurements: a change at line *p* of a Dockerfile rebuilds every layer
from *p* down, and a fast check placed first turns a 305-second failure into
a 5-second one.
