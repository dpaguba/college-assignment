import random

# Create an array with random numbers from 0 to 1
# This simulates binary numbers (0s and 1s)
random_array_1 = [random.randint(0, 1) for _ in range(random.randint(1, 10))]
print("Random array:", random_array_1)
random_array_2 = [random.randint(0, 1) for _ in range(random.randint(1, 10))]
print("Random array:", random_array_2)

def add_binary_numbers(bin1, bin2):
    """Adds two binary numbers represented as lists of 0s and 1s."""
    # Convert binary lists to strings, then to integers, and add them
    num1 = int(''.join(map(str, bin1)), 2)
    num2 = int(''.join(map(str, bin2)), 2)
    sum_num = num1 + num2
    
    # Convert the sum back to a binary list
    return list(map(int, bin(sum_num)[2:]))
# Add the two random binary numbers
result = add_binary_numbers(random_array_1, random_array_2)
print("Sum of binary numbers:", result)
# Modified 2025-08-11 10:24:29