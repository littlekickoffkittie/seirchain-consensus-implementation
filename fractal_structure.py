import os

def create_fractal_structure(base_path, level, max_level):
    """
    Recursively creates a fractal directory and file structure.
    """
    if level > max_level:
        return

    for i in range(3):
        # Create a directory for each branch of the fractal
        dir_path = os.path.join(base_path, f"branch_{i}")
        os.makedirs(dir_path, exist_ok=True)

        # Create a file in the directory
        file_path = os.path.join(dir_path, f"data_level_{level}.txt")
        with open(file_path, 'w') as f:
            f.write(f"This is data for level {level}, branch {i}.")

        # Recurse to the next level
        create_fractal_structure(dir_path, level + 1, max_level)

if __name__ == '__main__':
    base_dir = "fractal_file_system"
    max_depth = 2

    print(f"Creating a fractal file structure in '{base_dir}' with depth {max_depth}...")
    create_fractal_structure(base_dir, 1, max_depth)
    print("Fractal file structure created successfully.")
