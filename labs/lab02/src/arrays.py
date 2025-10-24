def min_max(nums: list[float | int]) -> tuple[float | int, float | int] | type[ValueError]:
    return (min(nums), max(nums)) if (len(nums) != 0) else ValueError

def unique_sorted(nums: list[float | int]) -> list[float | int]:    
    return sorted(list(set(nums)))

def flatten(mat: list[list | tuple]) -> list | type[TypeError]:
    output = []
    for obj in mat:
        if not isinstance(obj, tuple) and not isinstance(obj, list):
            return TypeError
        for val in obj:
            output.append(val)
    return output