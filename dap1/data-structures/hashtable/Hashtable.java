/**
 * A hash table with both collision strategies, from chapter eighteen.
 *
 * <p>Chaining puts colliding keys in a list at the bucket; open addressing
 * looks for the next free slot. The difference shows up on removal: a chain
 * can simply drop an entry, while an open table must leave a mark, because a
 * later key may have been placed past this slot and a genuine gap would end
 * the search too early.
 */
public class Hashtable {

    private static final double MAXIMUM_LOAD = 0.75;

    private final boolean openAddressing;
    private final boolean growing;
    private Entry[] buckets;
    private int count;

    /** A table using chaining. */
    public Hashtable(int capacity) {
        this(capacity, false);
    }

    /** A table using chaining or open addressing, growing as it fills. */
    public Hashtable(int capacity, boolean openAddressing) {
        this(capacity, openAddressing, true);
    }

    /**
     * A table that may be forbidden to grow.
     *
     * <p>A fixed table is what the lecture presents, and it is the only way
     * to see the structure degenerate: with growth switched on the load
     * factor keeps the chains short whatever the keys are, so the cost of a
     * bad hash function never becomes visible.
     */
    public Hashtable(int capacity, boolean openAddressing, boolean growing) {
        this.openAddressing = openAddressing;
        this.growing = growing;
        this.buckets = new Entry[Math.max(1, capacity)];
    }

    /** How many keys the table holds. */
    public int size() {
        return count;
    }

    /** The fraction of the table in use. */
    public double loadFactor() {
        return (double) count / buckets.length;
    }

    /** Stores a value under a key, replacing any earlier one. */
    public void put(String key, int value) {
        if (growing && loadFactor() >= MAXIMUM_LOAD) {
            grow();
        }
        if (openAddressing) {
            putOpen(buckets, key, value);
        } else {
            putChained(buckets, key, value);
        }
    }

    /** The value stored under the key, or null. */
    public Integer get(String key) {
        if (openAddressing) {
            int slot = findOpen(key);
            return slot < 0 ? null : buckets[slot].value;
        }
        for (Entry entry = buckets[bucketOf(key, buckets.length)]; entry != null;
                entry = entry.next) {
            if (entry.key.equals(key)) {
                return entry.value;
            }
        }
        return null;
    }

    /**
     * Removes a key.
     *
     * @return whether it was there
     */
    public boolean remove(String key) {
        if (openAddressing) {
            int slot = findOpen(key);
            if (slot < 0) {
                return false;
            }
            buckets[slot].removed = true;
            count--;
            return true;
        }
        int bucket = bucketOf(key, buckets.length);
        Entry previous = null;
        for (Entry entry = buckets[bucket]; entry != null; entry = entry.next) {
            if (entry.key.equals(key)) {
                if (previous == null) {
                    buckets[bucket] = entry.next;
                } else {
                    previous.next = entry.next;
                }
                count--;
                return true;
            }
            previous = entry;
        }
        return false;
    }

    /**
     * The length of the longest chain, or the longest run of occupied slots.
     *
     * <p>Measured rather than derived, because the quantity that decides how
     * fast a lookup is depends on the keys and on the hash function, not on
     * the number of entries. A table with one bucket degenerates into a
     * linear search and this method says so.
     */
    public int longestBucket() {
        int longest = 0;
        if (openAddressing) {
            int run = 0;
            for (int index = 0; index < buckets.length * 2; index++) {
                Entry entry = buckets[index % buckets.length];
                if (entry == null) {
                    run = 0;
                } else {
                    run++;
                    longest = Math.max(longest, run);
                }
            }
            return Math.min(longest, buckets.length);
        }
        for (Entry bucket : buckets) {
            int chain = 0;
            for (Entry entry = bucket; entry != null; entry = entry.next) {
                if (!entry.removed) {
                    chain++;
                }
            }
            longest = Math.max(longest, chain);
        }
        return longest;
    }

    /** How many entries a lookup of this key inspects. */
    public int probesFor(String key) {
        int probes = 0;
        if (openAddressing) {
            int slot = bucketOf(key, buckets.length);
            for (int step = 0; step < buckets.length; step++) {
                probes++;
                Entry entry = buckets[(slot + step) % buckets.length];
                if (entry == null || (!entry.removed && entry.key.equals(key))) {
                    break;
                }
            }
            return probes;
        }
        for (Entry entry = buckets[bucketOf(key, buckets.length)]; entry != null;
                entry = entry.next) {
            probes++;
            if (entry.key.equals(key)) {
                break;
            }
        }
        return probes;
    }

    private void grow() {
        Entry[] larger = new Entry[buckets.length * 2];
        for (Entry bucket : buckets) {
            for (Entry entry = bucket; entry != null; entry = entry.next) {
                if (!entry.removed) {
                    if (openAddressing) {
                        putOpen(larger, entry.key, entry.value);
                    } else {
                        putChained(larger, entry.key, entry.value);
                    }
                }
            }
        }
        int stored = count;
        buckets = larger;
        count = stored;
    }

    private void putChained(Entry[] table, String key, int value) {
        int bucket = bucketOf(key, table.length);
        for (Entry entry = table[bucket]; entry != null; entry = entry.next) {
            if (entry.key.equals(key)) {
                entry.value = value;
                return;
            }
        }
        Entry entry = new Entry(key, value);
        entry.next = table[bucket];
        table[bucket] = entry;
        if (table == buckets) {
            count++;
        }
    }

    private void putOpen(Entry[] table, String key, int value) {
        int slot = bucketOf(key, table.length);
        int firstFree = -1;
        for (int step = 0; step < table.length; step++) {
            int probe = (slot + step) % table.length;
            Entry entry = table[probe];
            if (entry == null) {
                int target = firstFree >= 0 ? firstFree : probe;
                table[target] = new Entry(key, value);
                if (table == buckets) {
                    count++;
                }
                return;
            }
            if (entry.removed && firstFree < 0) {
                firstFree = probe;
            }
            if (!entry.removed && entry.key.equals(key)) {
                entry.value = value;
                return;
            }
        }
        throw new IllegalStateException("table full");
    }

    private int findOpen(String key) {
        int slot = bucketOf(key, buckets.length);
        for (int step = 0; step < buckets.length; step++) {
            int probe = (slot + step) % buckets.length;
            Entry entry = buckets[probe];
            if (entry == null) {
                return -1;
            }
            if (!entry.removed && entry.key.equals(key)) {
                return probe;
            }
        }
        return -1;
    }

    private int bucketOf(String key, int length) {
        return Math.floorMod(key.hashCode(), length);
    }

    /** One stored key with its value, and the next entry of its chain. */
    private static class Entry {
        private final String key;
        private int value;
        private Entry next;
        private boolean removed;

        Entry(String key, int value) {
            this.key = key;
            this.value = value;
        }
    }
}
