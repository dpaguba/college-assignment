import random

# Create an array with random numbers from 1 to 100
random_array = [random.randint(1, 100) for _ in range(10)]  # Change 10 to desired array size

print("Random array:", random_array)

def insertion_sort_reverse(arr):
    """Sorts an array in reverse order using the insertion sort algorithm."""
    for i in range(1, len(arr)):
        # The current element to be inserted in the sorted part of the array
        key = arr[i]
        # Index of the previous element
        j = i - 1
        # Move elements of arr[0..i-1], that are less than key,
        # to one position ahead of their current position
        while j >= 0 and key > arr[j]:
            # Shift element to the right
            arr[j + 1] = arr[j]
            # Decrement j to check the next element
            j -= 1
        # Place the key in its correct position
        arr[j + 1] = key
    return arr

# Sort the random array in reverse order using insertion sort
sorted_array_reverse = insertion_sort_reverse(random_array.copy())
print("Sorted array in reverse order:", sorted_array_reverse)