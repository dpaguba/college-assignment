# Scopes and lifecycle

The default lifecycle is a sequence: validate, compile, test, package,
verify, install, deploy. Asking for one phase runs every phase before it,
which is why `install` also runs the tests and why there is no way to package
without compiling.

## Scopes

| scope | compile | test | runtime |
|---|---|---|---|
| compile | yes | yes | yes |
| provided | yes | yes | no |
| runtime | no | yes | yes |
| test | no | yes | no |

`provided` is the one worth understanding: the dependency is needed to
compile against but is already present where the artefact will run. Shipping
it anyway puts two copies of the same classes on the classpath, and which one
wins is not something the build decides.

Convention over configuration: sources in `src/main/java`, resources in
`src/main/resources`, tests in `src/test/java`, output in `target`. Following
the convention means the build file says only what is unusual.
