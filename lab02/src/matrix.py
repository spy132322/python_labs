def transpose(mat: list[list[float | int]]) -> list[list[float | int]] | type[ValueError]:
    if not mat:
        return []
    row_length = len(mat[0])    
    for item in mat:
        if len(item) != row_length: return ValueError
    return [[row[i] for row in mat] for i in range(row_length)]
def col_sum(mat: list[list[float | int]]) -> list[float] | type[ValueError]:
    if not mat: return []
    row_length = len(mat[0])
    for item in mat:
        if len(item) != row_length: return ValueError
    nmat = transpose(mat)
    return [sum(arr) for arr in nmat] # type: ignore

def row_sum(mat: list[list[float | int]]) -> list[float] | type[ValueError]:
    if not mat: return []
    row_length = len(mat[0])
    for item in mat:
        if len(item) != row_length: return ValueError
    return [sum(arr) for arr in mat]