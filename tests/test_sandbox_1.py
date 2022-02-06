import numpy as np
from operator import itemgetter
from line import *
import matplotlib.pyplot as plt
import matplotlib.colors as clr

n =10000
x = np.linspace(-1, 2, n)
max = np.max(x)
#max = 2e-5

#snorm = clr.SymLogNorm(linthresh = pow(10, -2 ), vmin = -max, vmax = max, base = 10)
#y = snorm.__call__(x)
#plt.figure()
#plt.plot(x,y)

#snorm = clr.SymLogNorm(linthresh = pow(10, -4 ), linscale = 0.0000000001, vmin = -max, vmax = max, base = 10)
#y = snorm.__call__(x)
#plt.plot(x,y)

y=np.linspace(-1,2,n)

#y = np.ones((100,100))
#y[10,:]=np.linspace(-1,2,100)
#y[11,:]=np.linspace(-1,2,100)
#y[12,:]=np.linspace(-1,2,100)

decades = 2
max = np.max(y)
min = np.min(y)
pos = y >= pow(10, -decades)
neg = y <= -pow(10, -decades)
y[np.abs(y) < pow(10, -decades)] = 0.5
y[pos] = np.interp(np.log10(y[pos]), (-decades, np.log10(max)), (0.5, 1.0))
y[neg] = np.interp(np.log10(np.abs(y[neg])), (-decades, np.log10(np.abs(min))), (0.5, 0.0))
plt.plot(x,y)
#plt.imshow(y, cmap = 'bwr')
plt.show()