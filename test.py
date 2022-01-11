import numpy as np
from operator import itemgetter
from line import *
import matplotlib.pyplot as plt
import matplotlib.colors as clr

n =1000
x = np.linspace(0, 2, n)
fig     = plt.figure()
snorm = clr.SymLogNorm(linthresh = pow(10, (-1*3) ), vmin = -1, vmax = 0.5)
y = snorm.__call__(x)
#plt.plot(x,y)
#plt.show()

norm = clr.LogNorm()
a = np.array([[1, 2], [3, 4]])
shape = np.shape(a)
print(shape)
print(a)
a.flatten()
#a = norm.__call__(a)
print(a)
a = np.reshape(a,shape)
print(a)
