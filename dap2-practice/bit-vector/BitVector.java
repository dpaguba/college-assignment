/**
 * A bit vector packed into an int array.
 *
 * <p>Sheet 9, task 9.1a. n bits in ceil(n/32) integers, so the whole structure
 * costs n + at most 31 bits of payload plus the object header, well inside the
 * n + 3200 the sheet allows.
 *
 * <p>The obvious {@code boolean[]} would take a whole byte per entry, eight
 * times more, because the JVM has no addressable unit smaller than a byte. That
 * factor of eight is the entire point of the exercise.
 */
public class BitVector {

    private final int size;
    private final int[] words;

    /** All n bits start at 0. */
    public BitVector(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("the length must not be negative");
        }
        this.size = n;
        this.words = new int[(n + 31) / 32];
    }

    /** The number of bits stored. */
    public int size() {
        return size;
    }

    /**
     * The bit at the given position.
     *
     * <p>Position j lives in word j/32 at bit j%32, both of which are a shift
     * and a mask because 32 is a power of two.
     */
    public boolean get(int index) {
        checkRange(index);
        return (words[index >>> 5] & (1 << (index & 31))) != 0;
    }

    /**
     * Sets the bit at the given position.
     *
     * <p>Setting is an OR with a one-bit mask, clearing is an AND with its
     * complement. Neither touches the other 31 bits in the word.
     */
    public void set(int index, boolean value) {
        checkRange(index);
        int mask = 1 << (index & 31);
        if (value) {
            words[index >>> 5] |= mask;
        } else {
            words[index >>> 5] &= ~mask;
        }
    }

    /** The raw word, for the rank structure that has to count whole words at a time. */
    int word(int wordIndex) {
        return words[wordIndex];
    }

    /** How many words the vector occupies. */
    int wordCount() {
        return words.length;
    }

    private void checkRange(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("position " + index + " outside [0, " + size + ")");
        }
    }
}
