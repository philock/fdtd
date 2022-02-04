import numpy as np
import matplotlib.pyplot as plt

#x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#print(x[0,0])

#a = (slice(None), slice(1,3))
#print(x[a])

x = np.array([[1, 2, 3], [4, 5, 6]])
a = np.linspace(1,2,2)
#print(x)
print(a)
print(np.shape(a))
a = a[:,None]
print(a)
print(np.shape(a))
print(x*a)