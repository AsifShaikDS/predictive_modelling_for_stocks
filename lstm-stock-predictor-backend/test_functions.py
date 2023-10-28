def get_shape(my_list):
    if isinstance(my_list, list):
        if all(isinstance(sublist, list) for sublist in my_list):
            # It's a 2D list
            num_rows = len(my_list)
            num_cols = len(my_list[0]) if num_rows > 0 else 0
            return (num_rows, num_cols)
        else:
            # It's a 1D list
            num_rows = len(my_list)
            return (num_rows, 1)
    else:
        # It's not a list
        return None

# Example usage:
my_list_1d = [1, 2, 3, 4]
shape_1d = get_shape(my_list_1d)
print(f"Shape of 1D list: {shape_1d}")

my_list_2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
shape_2d = get_shape(my_list_2d)
print(f"Shape of 2D list: {shape_2d}")
