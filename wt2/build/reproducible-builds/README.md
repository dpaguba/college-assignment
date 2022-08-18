# Reproducible builds

A version is reproducible when it always names the same artefact. `1.2.3` is;
`[1.0,2.0)`, `1.0-SNAPSHOT`, `LATEST` and `RELEASE` are not.

The module measures what that means. With the range `[1.0,2.0)` and versions
1.0 and 1.1 in the repository, the build resolves 1.1. Later, with 1.2 also
published, the same project file resolves 1.2. Nothing in the project
changed, and the artefact did.

A lock file removes the drift by writing down the whole resolved graph. The
project file then says what is wanted and the lock file says what was used.

## Bit-for-bit

The same sources hash to the same artefact, and the module checks that the
order in which the files are read does not matter. Adding a timestamp changes
the hash, which is the most common reason two builds of identical sources
produce different bytes, along with file ordering and absolute paths.
