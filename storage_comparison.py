import matplotlib.pyplot as plt
import numpy as np

def linear_storage(n):
  """
  Calculates the storage requirement for a linear blockchain.
  Assumes each transaction has a fixed size.
  """
  return n

def fractal_storage(n):
  """
  Calculates the storage requirement for a fractal blockchain (SeirChain).
  The storage grows sub-linearly, proportional to log(n).
  """
  return np.log(n)

if __name__ == '__main__':
  # Number of transactions
  transactions = np.arange(1, 10000)

  # Calculate storage for both models
  linear = linear_storage(transactions)
  fractal = fractal_storage(transactions)

  # Plot the results
  plt.figure(figsize=(10, 6))
  plt.plot(transactions, linear, label="Linear Blockchain")
  plt.plot(transactions, fractal, label="SeirChain (Fractal)")
  plt.xlabel("Number of Transactions")
  plt.ylabel("Storage Requirements (Arbitrary Units)")
  plt.title("Storage Requirements: Linear vs. Fractal Blockchain")
  plt.legend()
  plt.grid(True)
  plt.savefig("storage_comparison.png")
  plt.show()
