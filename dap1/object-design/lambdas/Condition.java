/**
 * A functional interface: one abstract method, so a lambda can stand for it.
 *
 * <p>The lambda in the calling code has no type of its own. It takes the type
 * of the interface the context expects, which is why a single method is
 * required: with two, there would be nothing to say which one the lambda is.
 */
public interface Condition {

    /** Whether the value satisfies the condition. */
    boolean holds(int value);
}
