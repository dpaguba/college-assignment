# Dependency injection

A service is handed in rather than constructed. Within one injector every
service is built once, so two requests return the same instance.

Injectors form a tree. A child sees everything its parent provides and can
shadow any of it without affecting the parent, which is how a component can
be given its own copy of a service while everything else keeps the shared
one.

Dependencies are resolved recursively: a greeter that needs a clock gets the
clock built first. A cycle is reported as an error rather than recursed into,
because the alternative is a stack overflow with no indication of which two
services caused it.

What it buys: a test can hand in a substitute, the caller does not need to
know how a service is built, one instance can be shared without a global, and
the wiring lives in one place.
