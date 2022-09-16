# Build and dependency management

Three questions a build tool answers: which version of a transitively
required artefact is used, when a dependency is on the classpath, and whether
building the same sources twice gives the same result.

The resolution rule is nearest wins with the first declaration breaking ties,
which is checked here against an independent search.
