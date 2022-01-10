/**
 * What can be written once an iterator exists.
 *
 * <p>Neither method below knows which structure it is walking, and both
 * would keep working for a structure written afterwards. That is what the
 * pattern buys: the traversal is separated from the thing traversed, so
 * algorithms and containers stop multiplying against each other.
 */
public class Iterators {

    /** The values as one text, in iteration order. */
    public static <T> String collect(Iterator<T> iterator) {
        StringBuilder text = new StringBuilder();
        while (iterator.hasNext()) {
            text.append(iterator.next());
        }
        return text.toString();
    }

    /**
     * Whether two iterators produce the same values in the same order.
     *
     * <p>The exercise asks for it over two lists, and writing it over
     * iterators instead means it also compares a list with a tree walk, or
     * either with the multi-list iterator.
     */
    public static <T> boolean sameContent(Iterator<T> first, Iterator<T> second) {
        while (first.hasNext() && second.hasNext()) {
            T left = first.next();
            T right = second.next();
            if (left == null ? right != null : !left.equals(right)) {
                return false;
            }
        }
        return !first.hasNext() && !second.hasNext();
    }

    /** How many values an iterator yields. */
    public static <T> int count(Iterator<T> iterator) {
        int values = 0;
        while (iterator.hasNext()) {
            iterator.next();
            values++;
        }
        return values;
    }
}
