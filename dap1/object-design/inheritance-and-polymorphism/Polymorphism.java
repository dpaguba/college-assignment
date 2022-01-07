import java.util.List;

/**
 * What the two types of an expression each decide.
 *
 * <p>An object has a static type, known to the compiler, and a dynamic type,
 * known only while the program runs. Overriding is resolved by the dynamic
 * type and overloading by the static one, so the two methods below disagree
 * about the same object, and both are behaving correctly.
 */
public class Polymorphism {

    /** Whether the object is a person, which every student also is. */
    public static boolean isPerson(Object candidate) {
        return candidate instanceof Person;
    }

    /** The overload chosen when the expression has the type Person. */
    public static String greet(Person person) {
        return "greeting a person";
    }

    /** The overload chosen when it has the type Student. */
    public static String greet(Student student) {
        return "greeting a student";
    }

    /**
     * Describes each element through the base type.
     *
     * <p>The loop knows nothing about students, and students still describe
     * themselves, which is the reason the hierarchy exists.
     */
    public static String describeAll(List<Person> people) {
        StringBuilder text = new StringBuilder();
        for (Person person : people) {
            if (text.length() > 0) {
                text.append("|");
            }
            text.append(person.describe());
        }
        return text.toString();
    }
}
