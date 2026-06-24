import numpy as np

# This code demonstrates the creation and manipulation of a 2D array using NumPy.
numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
array = np.array(numbers)
print(array)
print(f"Array dimension: {array.ndim}")
print(f"Array shape: {array.shape}")

print(f"Element at row 1, column 2: {array[0, 1]}")
print(f"Element at row 3, column 1: {array[2, 0]}")
print(f"First row: {array[0, :]}")
print(f"First column: {array[:, 0]}")


# This code demonstrates the creation and manipulation of a 3D array using NumPy.
numbers_3d = [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]
array_3d = np.array(numbers_3d)
print(array_3d)
print(f"3D Array dimension: {array_3d.ndim}")
print(f"3D Array shape: {array_3d.shape}")