import random

# Create an array with random numbers from 1 to 100
random_array = [random.randint(-100, 100) for _ in range(10)]

def max_sum(arr):
    """
    Function to find the maximum sum of any contiguous subarray in the array.
    This function returns the maximum sum and the row (subarray) that produces this sum.
    """
    if not arr:
        return 0
    
    max_sum_value = float('-inf')
    max_row = []
    for index_i, i in random_array:
        for index_j, j in random_array:
            current_sum = 0
            k=index_i
            while k <= index_j:
                current_sum += random_array[k]
                k += 1
            if current_sum > max_sum_value:
                max_sum_value = current_sum
                max_row = random_array[index_i:index_j+1]
    return max_sum_value, max_row


# Example usage
print("Random Array:", random_array)
result, row = max_sum(random_array)
print("Maximum Sum:", result)
print("Row with Maximum Sum:", row)
    
