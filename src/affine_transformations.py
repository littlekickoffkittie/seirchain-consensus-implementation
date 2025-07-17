import numpy as np

def f1(p):
  """
  Transformation 1: Scale by 1/2 and move to the bottom-left.
  """
  A = np.array([[0.5, 0], [0, 0.5]])
  b = np.array([0, 0])
  return np.dot(A, p) + b

def f2(p):
  """
  Transformation 2: Scale by 1/2 and move to the bottom-right.
  """
  A = np.array([[0.5, 0], [0, 0.5]])
  b = np.array([0.5, 0])
  return np.dot(A, p) + b

def f3(p):
  """
  Transformation 3: Scale by 1/2 and move to the top.
  """
  A = np.array([[0.5, 0], [0, 0.5]])
  b = np.array([0.25, 0.5 * (3**0.5 / 2)])
  return np.dot(A, p) + b

if __name__ == '__main__':
  # Starting point
  p = np.array([0, 0])

  # Apply transformations
  p1 = f1(p)
  p2 = f2(p)
  p3 = f3(p)

  print(f"Original point: {p}")
  print(f"After f1: {p1}")
  print(f"After f2: {p2}")
  print(f"After f3: {p3}")

  # You can also use these transformations to generate the Sierpinski triangle
  # by iterating and randomly choosing a transformation.
