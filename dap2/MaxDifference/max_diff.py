import random

# Create an array with random numbers from 1 to 100
random_array = [random.randint(0, 100) for _ in range(10)]
def max_difference(arr):
    """
    Function to find the maximum difference between any two elements in the array.
    """
    if not arr:
        return 0
    
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                max_diff = arr[i] - arr[j]
            else:
                max_diff = arr[j] - arr[i]
            if 'max_difference' not in locals() or max_diff > max_difference:
                max_difference = max_diff
    return max_difference if 'max_difference' in locals() else 0


# Example usage
print("Random Array:", random_array)
result = max_difference(random_array)
print("Maximum Difference:", result)

# Modified 2025-08-11 10:24:29