from fdtd import line
import numpy as np
import matplotlib.pyplot as plt
pltrows = 3
pltcols =3

m_smaller_1 = line(0,0,90,100)
grid = m_smaller_1.render()
#print(grid)
plt.subplot(pltrows,pltcols,1)
plt.title('m<1')
plt.imshow(grid, cmap='hot', interpolation='nearest')


m_larger_1 = line(0,0,100,90)
grid = m_larger_1.render()
#print(grid)
plt.subplot(pltrows,pltcols,2)
plt.title('m>1')
plt.imshow(grid, cmap='hot', interpolation='nearest')

xa_larger_xb = line(10,0,0,10)
grid = xa_larger_xb.render()
plt.subplot(pltrows,pltcols,3)
plt.title('xb<xa')
plt.imshow(grid, cmap='hot', interpolation='nearest')

xa_larger_xb = line(0,10,10,0)
grid = xa_larger_xb.render()
plt.subplot(pltrows,pltcols,4)
plt.title('yb<ya')
plt.imshow(grid, cmap='hot', interpolation='nearest')

xa_larger_xb = line(10,10,0,0)
grid = xa_larger_xb.render()
print(grid)
#print(np.shape(grid))
plt.subplot(pltrows,pltcols,5)
plt.title('xb<xa yb<ya')
plt.imshow(grid, cmap='hot', interpolation='nearest')

xa_larger_xb = line(10,5,20,5)
gridh = xa_larger_xb.render()
print(gridh)
#print(np.shape(gridh))
plt.subplot(pltrows,pltcols,5)
plt.title('horizontal')
plt.imshow(gridh, cmap='hot', interpolation='nearest')

xa_larger_xb = line(10,5,10,15)
grid = xa_larger_xb.render()
print(grid)
plt.subplot(pltrows,pltcols,6)
plt.title('vertical')
plt.imshow(grid, cmap='hot', interpolation='nearest')

print(np.logical_or(grid,gridh))

plt.show()