/** The base class of chapter eight. */
public class Person {

    private final String name;

    /** A person with a name. */
    public Person(String name) {
        this.name = name;
    }

    /** The name. */
    public String getName() {
        return name;
    }

    /** A description, which subclasses are expected to refine. */
    public String describe() {
        return "Person " + name;
    }

    @Override
    public boolean equals(Object other) {
        if (other == null || other.getClass() != getClass()) {
            return false;
        }
        return name.equals(((Person) other).name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }
}
