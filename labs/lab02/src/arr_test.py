import arrays
# Tests for min_max func
print('Testing min_max function')
print(f"[3, -1, 5, 5, 0] Out:", arrays.min_max([3, -1, 5, 5, 0]))
print(f"[42] Out:", arrays.min_max([42]))
print(f"[-5, -2 ,-9] Out:", arrays.min_max([-5, -2 ,-9]))
print(f"[] Out:", arrays.min_max([]))
print(f"[1.5, 2, 2.0, -3.1] Out:", arrays.min_max([1.5, 2, 2.0, -3.1]))

# Tests for unique_sorted
print('Testing unique_sorted')
print(f"[3, 1, 2, 1, 3] Out:", arrays.unique_sorted([3, 1, 2, 1, 3]))
print(f"[] Out:", arrays.unique_sorted([]))
print(f"[-1, -1, 0, 2, 2] Out:", arrays.unique_sorted([-1, -1, 0, 2, 2]))
print(f"[1.0, 1, 2.5, 2.5, 0] Out:", arrays.unique_sorted([1.0, 1, 2.5, 2.5, 0]))

# Tests for flatten
print('Tesing flatten function')
print(f"[[1, 2], [3, 4]] Out:", arrays.flatten([[1, 2], [3, 4]]))
print(f"[[1, 2], (3, 4, 5)] Out:", arrays.flatten([[1, 2], (3, 4, 5)]))
print(f"[[1], [], [2, 3]] Out:", arrays.flatten([[1], [], [2, 3]]))
print(f"[[1, 2], \"ab\"] Out:", arrays.flatten([[1, 2], "ab"])) # type: ignore


