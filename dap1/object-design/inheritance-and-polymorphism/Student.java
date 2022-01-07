/**
 * The subclass of chapter eight, which adds a field and refines a method.
 *
 * <p>The description is overridden, so a call through a variable of type
 * {@code Person} still runs this version. Comparing classes rather than using
 * {@code instanceof} in {@code equals} is what keeps that relation
 * symmetric: a person is never equal to a student, in either direction.
 */
public class Student extends Person {

    private final int matriculation;

    /** A student with a name and a matriculation number. */
    public Student(String name, int matriculation) {
        super(name);
        this.matriculation = matriculation;
    }

    /** The matriculation number. */
    public int getMatriculation() {
        return matriculation;
    }

    @Override
    public String describe() {
        return "Student " + getName() + " (" + matriculation + ")";
    }

    /** The base version, reached through super. */
    public String describeAsPerson() {
        return super.describe();
    }

    @Override
    public boolean equals(Object other) {
        return super.equals(other) && matriculation == ((Student) other).matriculation;
    }

    @Override
    public int hashCode() {
        return 31 * super.hashCode() + matriculation;
    }
}
