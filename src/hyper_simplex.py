import matplotlib.pyplot as plt
import numpy as np

def get_sierpinski_points(level, vertices):
    """
    Recursively generates points for a Sierpinski-like structure.
    """
    if level == 0:
        return [tuple(v) for v in vertices]

    # Get the midpoints of the triangle sides
    p1 = (vertices[0] + vertices[1]) / 2
    p2 = (vertices[1] + vertices[2]) / 2
    p3 = (vertices[2] + vertices[0]) / 2

    points = []
    # Recurse on the three smaller triangles
    points.extend(get_sierpinski_points(level - 1, [vertices[0], p1, p3]))
    points.extend(get_sierpinski_points(level - 1, [p1, vertices[1], p2]))
    points.extend(get_sierpinski_points(level - 1, [p3, p2, vertices[2]]))

    return points

if __name__ == '__main__':
    levels = 3  # Number of recursion levels

    # Initial triangle vertices
    initial_vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(0.75)]])

    plt.figure(figsize=(10, 10))

    for level in range(levels + 1):
        points = get_sierpinski_points(level, initial_vertices)
        x, y = zip(*points)

        plt.subplot(2, 2, level + 1)
        plt.scatter(x, y, s=10)
        plt.title(f"Hyper-simplex Model: Level {level}")
        plt.axis("equal")
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("hyper_simplex_simulation.png")
    plt.show()
