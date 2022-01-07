/**
 * An interface with a default method, from chapter thirteen.
 *
 * <p>A default method lets an interface gain a method without breaking the
 * classes that already implement it. The implementing class may still
 * override it, so the default is a starting point rather than a rule.
 */
public interface Sink {

    /** The prefix each implementation supplies. */
    String label();

    /** The report, assembled from the label and the count. */
    default String report(int count) {
        return label() + " " + count;
    }
}
