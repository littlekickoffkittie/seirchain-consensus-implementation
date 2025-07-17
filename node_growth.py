import math

def node_growth(N, m):
  """
  Calculates the number of nodes in a Triad Matrix.
  |V_{N,m}| ≈ 2^(m-2)N^m

  Args:
    N: The number of nodes in the initial cluster.
    m: The number of levels in the fractal structure.

  Returns:
    The approximate number of nodes in the Triad Matrix.
  """
  return (2**(m - 2)) * (N**m)

if __name__ == '__main__':
  N = 3  # Number of nodes in the initial cluster
  m = 4  # Number of levels in the fractal structure

  num_nodes = node_growth(N, m)

  print(f"For N = {N} and m = {m}, the approximate number of nodes is: {num_nodes}")

  print("\nExplanation of N and m:")
  print("N: Represents the number of nodes in the initial cluster of the Triad Matrix. It's the base unit that is replicated at each level.")
  print("m: Represents the number of levels or recursive steps in the fractal construction of the Triad Matrix. It determines the scale of the structure.")
