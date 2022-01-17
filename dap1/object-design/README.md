# Object design

| Topic | |
|---|---|
| [rational-numbers](rational-numbers/) | a class that can keep a promise |
| [inheritance-and-polymorphism](inheritance-and-polymorphism/) | which type decides what |
| [interfaces-and-generics](interfaces-and-generics/) | stating what a method needs |
| [lambdas](lambdas/) | behaviour as a value |

Four chapters that build one idea: a type is a promise, and the language
features here are ways of stating and keeping one.

The fraction promises to be normalised, which holds because nothing outside
can write a field. It also shows what a promise costs, since exact arithmetic
has a range and the class now says so instead of wrapping around silently.

The hierarchy promises that every `Person` can describe itself, which is why a
loop needs no case for students. Generics promise that whatever comes out of
the stack is what went in. An interface promises a method exists, and a lambda
is the shortest way to supply one.
