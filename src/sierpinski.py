import matplotlib.pyplot as plt
import random

def get_mid(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def sierpinski(n):
    """
    Generates and plots the Sierpinski Triangle using the chaos game method.
    n: number of points to plot.
    """
    # Vertices of the triangle
    vertices = [(0, 0), (1, 0), (0.5, 3**0.5 / 2)]

    # Starting point
    x, y = (0, 0)

    # Lists to store the coordinates of the points
    x_coords = [x]
    y_coords = [y]

    for _ in range(n):
        # Choose a random vertex
        chosen_vertex = random.choice(vertices)

        # Get the midpoint
        x, y = get_mid((x, y), chosen_vertex)

        # Add the new point to the lists
        x_coords.append(x)
        y_coords.append(y)

    # Plot the points
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=1)
    plt.title("Sierpinski Triangle")
    plt.axis("off")
    plt.savefig("sierpinski_triangle.png")
    plt.show()

def hausdorff_dimension():
    """
    Calculates the Hausdorff dimension of the Sierpinski Triangle.
    D = log(N) / log(s)
    N = number of self-similar copies = 3
    s = scaling factor = 2
    """
    import math
    return math.log(3) / math.log(2)

if __name__ == '__main__':
    sierpinski(50000)
    print(f"Hausdorff dimension of the Sierpinski Triangle: {hausdorff_dimension()}")
