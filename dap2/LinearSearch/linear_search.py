import random

# Create an array with random numbers from 1 to 100
random_array = [random.randint(1,100) for _ in range(10)] # Change 10 to desired array size

print("Random array:", random_array)

def linear_search(arr, target):
    """Searches for a target value in an array using linear search algorithm."""
    for index, value in enumerate(arr):
        if value == target:
            return index  # Return the index of the found element
    return -1  # Return -1 if the target is not found

# Perform linear search on the random array
target_value = random.randint(1, 100)  # Randomly select a target
print(f"Searching for {target_value} in the array...")
index = linear_search(random_array, target_value)
if index != -1:
    print(f"Value {target_value} found at index {index}.")
else:
    print(f"Value {target_value} not found in the array.")