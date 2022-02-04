import numpy as np
import matplotlib.pyplot as plt

x = np.array([[1, 2, 3], [4, 5, 6]])
print(x)
a = (slice(None), slice(0, -1))
print(x[a])