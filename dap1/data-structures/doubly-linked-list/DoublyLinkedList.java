/**
 * The doubly linked list of chapter nine, with the course's element class.
 *
 * <p>Each element knows its predecessor and its successor, so a removal needs
 * no search for the element before it, and the list keeps a reference to both
 * ends so that appending is as cheap as prepending. The size is stored rather
 * than counted, which is the usual trade of one field against a walk.
 *
 * <p>The element class is private and static: private because no caller
 * should hold one, static because an element needs nothing from the list it
 * happens to sit in.
 */
public class DoublyLinkedList<T> implements Iterable<T> {

    private Element first;
    private Element last;
    private int size;

    /** How many values the list holds. */
    public int size() {
        return size;
    }

    /** Whether it holds none. */
    public boolean isEmpty() {
        return size == 0;
    }

    /** Adds a value at the end. */
    public void append(T value) {
        Element element = new Element(value);
        if (last == null) {
            first = element;
            last = element;
        } else {
            last.connectAsSucc(element);
            last = element;
        }
        size++;
    }

    /** Adds a value at the front. */
    public void prepend(T value) {
        Element element = new Element(value);
        if (first == null) {
            first = element;
            last = element;
        } else {
            first.connectAsPred(element);
            first = element;
        }
        size++;
    }

    /** The first value, or null when the list is empty. */
    public T first() {
        return first == null ? null : first.getContent();
    }

    /** The last value, or null when the list is empty. */
    public T last() {
        return last == null ? null : last.getContent();
    }

    /** Whether the value occurs in the list. */
    public boolean contains(T value) {
        for (Element element = first; element != null; element = element.getSucc()) {
            if (equal(element.getContent(), value)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Removes the first occurrence of the value.
     *
     * @return whether anything was removed
     */
    public boolean remove(T value) {
        for (Element element = first; element != null; element = element.getSucc()) {
            if (equal(element.getContent(), value)) {
                unlink(element);
                return true;
            }
        }
        return false;
    }

    /**
     * Turns the list around by exchanging the two links of every element.
     *
     * <p>No value moves and no element is created. Reversing a singly linked
     * list needs a loop that remembers three positions; here the operation is
     * the same swap at every element, which is one of the reasons the second
     * link is worth its memory.
     */
    public void reverse() {
        Element current = first;
        while (current != null) {
            Element following = current.succ;
            current.succ = current.pred;
            current.pred = following;
            current = following;
        }
        Element held = first;
        first = last;
        last = held;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private Element position = first;

            @Override
            public boolean hasNext() {
                return position != null;
            }

            @Override
            public T next() {
                T value = position.getContent();
                position = position.getSucc();
                return value;
            }
        };
    }

    /** An iterator that starts at the end, used by the reverse iterator. */
    public Iterator<T> backwardIterator() {
        return new Iterator<T>() {
            private Element position = last;

            @Override
            public boolean hasNext() {
                return position != null;
            }

            @Override
            public T next() {
                T value = position.getContent();
                position = position.getPred();
                return value;
            }
        };
    }

    @Override
    public String toString() {
        StringBuilder text = new StringBuilder("[");
        for (Element element = first; element != null; element = element.getSucc()) {
            if (element != first) {
                text.append(", ");
            }
            text.append(element.getContent());
        }
        return text.append("]").toString();
    }

    /**
     * Hands every value to the strategy, in order.
     *
     * <p>The list decides how to walk itself and the strategy decides what to
     * do with each value, so a new computation is a new class and never a
     * change here. The tenth sheet asks for fourteen of them.
     */
    public void traverse(Strategy<T> strategy) {
        for (Element element = first; element != null; element = element.getSucc()) {
            strategy.handle(element.getContent());
        }
    }

    /** Replaces every value by what the transformation returns. */
    public void transformAll(Transformation<T> transformation) {
        for (Element element = first; element != null; element = element.getSucc()) {
            element.setContent(transformation.transform(element.getContent()));
        }
    }

    /**
     * Removes the values the strategy rejects.
     *
     * <p>The predecessor passed to the strategy is the one from the original
     * list, not the last value kept, because a removal must not change the
     * decision about the values after it. Reading the predecessor before any
     * unlinking is what keeps that true.
     *
     * @return how many values were removed
     */
    public int removeAll(Removal<T> removal) {
        int removed = 0;
        T predecessor = null;
        Element element = first;
        while (element != null) {
            Element following = element.getSucc();
            T value = element.getContent();
            if (removal.removes(value, predecessor)) {
                unlink(element);
                removed++;
            }
            predecessor = value;
            element = following;
        }
        return removed;
    }

    /**
     * Inserts a new value behind every element the strategy selects.
     *
     * <p>The inserted element is skipped, so a strategy that selects
     * everything terminates instead of inserting behind its own insertions.
     */
    public void insertBehindSelected(InsertionStrategy<T> strategy) {
        Element element = first;
        while (element != null) {
            Element following = element.getSucc();
            T value = element.getContent();
            if (strategy.select(value)) {
                Element inserted = new Element(strategy.insert(value));
                element.connectAsSucc(inserted);
                if (element == last) {
                    last = inserted;
                }
                size++;
            }
            element = following;
        }
    }

    /** A computation that is handed one value at a time. */
    public interface Strategy<T> {
        /** Handles the next value. */
        void handle(T value);
    }

    /** A replacement for a value. */
    public interface Transformation<T> {
        /** The value that replaces this one. */
        T transform(T value);
    }

    /** A decision about whether a value stays. */
    public interface Removal<T> {
        /** Whether to remove this value, given its predecessor in the original list. */
        boolean removes(T value, T predecessor);
    }

    /** A decision about what to insert behind a value. */
    public interface InsertionStrategy<T> {
        /** Whether something is inserted behind this value. */
        boolean select(T reference);

        /** The value to insert. */
        T insert(T reference);
    }

    private void unlink(Element element) {
        Element before = element.getPred();
        Element after = element.getSucc();
        if (before == null) {
            first = after;
        } else {
            before.succ = after;
        }
        if (after == null) {
            last = before;
        } else {
            after.pred = before;
        }
        element.pred = null;
        element.succ = null;
        size--;
    }

    private boolean equal(T left, T right) {
        return left == null ? right == null : left.equals(right);
    }

    /** One position in the list, holding a value and both neighbours. */
    private class Element {

        private T content;
        private Element pred;
        private Element succ;

        Element(T content) {
            this.content = content;
        }

        T getContent() {
            return content;
        }

        void setContent(T content) {
            this.content = content;
        }

        boolean hasSucc() {
            return succ != null;
        }

        Element getSucc() {
            return succ;
        }

        void connectAsSucc(Element element) {
            element.pred = this;
            element.succ = succ;
            if (succ != null) {
                succ.pred = element;
            }
            succ = element;
        }

        void disconnectSucc() {
            if (succ != null) {
                succ.pred = null;
                succ = null;
            }
        }

        boolean hasPred() {
            return pred != null;
        }

        Element getPred() {
            return pred;
        }

        void connectAsPred(Element element) {
            element.succ = this;
            element.pred = pred;
            if (pred != null) {
                pred.succ = element;
            }
            pred = element;
        }

        void disconnectPred() {
            if (pred != null) {
                pred.succ = null;
                pred = null;
            }
        }
    }
}
