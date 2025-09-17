import matrix
# Tests fot transpose
print('Testing transpose func')
print(f"[[1, 2, 3]] Out:", matrix.transpose([[1, 2, 3]]))
print(f"[[1], [2], [3]] Out:", matrix.transpose([[1], [2], [3]]))
print(f"[[1, 2], [3, 4]] Out:", matrix.transpose([[1, 2], [3, 4]]))
print(f"[] Out:", matrix.transpose([]))
print(f"[[1, 2], [3]] Out:", matrix.transpose([[1, 2], [3]]))
# Tests for row_sums
print('Testing row_summ')
print(f'[[1, 2, 3], [4, 5, 6]] Out:', matrix.row_sum([[1, 2, 3], [4, 5, 6]]))
print(f'[[-1, 1], [10, -10]] Out:', matrix.row_sum([[-1, 1], [10, -10]]))
print(f'[[0, 0], [0, 0]] Out:', matrix.row_sum([[0, 0], [0, 0]]))
print(f'[[1, 2], [3]] Out:', matrix.row_sum([[1, 2], [3]]))
# Test for col_sums
print('Testing col_summ')
print(f'[[1, 2, 3], [4, 5, 6]] Out:', matrix.col_sum([[1, 2, 3], [4, 5, 6]]))
print(f'[[-1, 1], [10, -10]] Out:', matrix.col_sum([[-1, 1], [10, -10]]))
print(f'[[0, 0], [0, 0]] Out:', matrix.col_sum([[0, 0], [0, 0]]))
print(f'[[1, 2], [3]] Out:', matrix.col_sum([[1, 2], [3]]))
