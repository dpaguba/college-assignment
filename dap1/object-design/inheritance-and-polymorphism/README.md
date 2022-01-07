# Inheritance and polymorphism

Chapter eight, and one question that catches everyone once.

```java
Person asPerson = new Student("Rae", 123456);

asPerson.describe();          // "Student Rae (123456)"
Polymorphism.greet(asPerson); // "greeting a person"
```

Same object, two answers. Overriding is resolved by the dynamic type, the
class the object actually has, and overloading is resolved by the static type,
the type the compiler sees in the expression. Both lines are correct and they
disagree, which is why a method that is overloaded on a hierarchy is a place
where a program can be right and unreadable at the same time.

The useful half is the first line. A loop over a list of `Person` calls
`describe` and each object answers for itself, so adding a new subclass adds
no case to any loop. That is what the hierarchy is for, and it is the same
mechanism the strategy pattern uses two chapters later.

## Equality across a hierarchy

`equals` implemented with `instanceof` breaks symmetry: a person can accept a
student while the student rejects the person, and a collection then answers
differently depending on which object it asks. Comparing `getClass()` keeps
the relation symmetric, at the cost of saying that a student is never equal to
a person even when the names match, which is the accurate answer for two objects
with different fields.

`super.describe()` is the other half of the chapter: a subclass can refine a
method and still reach the version it replaced, which is what makes extending
behaviour different from replacing it.
