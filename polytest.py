from math import *
import numpy as np
from line import *
from polygon import *
import matplotlib.pyplot as plt
import time

pltrows = 3
pltcols = 3

'''Square with corner taken out'''
a = (0,0)
b = (10,0)
c = (10,10)
d = (5,15)
square = polygon()
square.add_vertex(a)
square.add_vertex(b)
square.add_vertex(c)
square.add_vertex(a)

#square.set_vertex_list([(3,3), (10,3), (10,10), (7,10), (7,5), (3,5), (3,3)])
grid = square.render_outline()
#put inside of global grid
global_grid = np.zeros((20,20), dtype=bool)
global_grid[square.y : square.y + square.height  ,  square.x : square.x + square.width] = (square.grid != 0)
plt.subplot(pltrows,pltcols,1)
plt.imshow(global_grid, cmap='hot', interpolation='nearest')


'''Long and thin polygon'''
poly = polygon()
vertecies = [(1,2), (40, 60), (10,25), (1,2)]
for v in vertecies:
    poly.add_vertex(v)
#start = time.time()
grid = poly.render_filled()
#print(time.time() - start)
plt.subplot(pltrows,pltcols,2)
plt.imshow(grid, cmap='hot', interpolation='nearest')


'''Circle'''
circle = polygon()
R = 100
ang = np.linspace(0, 2*pi, 80)
for a in ang:
    circle.add_vertex(( int(R*cos(a)) + R, int(R*sin(a)) + R))

avgtime =0
for i in range(3):
    start = time.time()
    grid = circle.render_filled()
    avgtime += (time.time() - start)
    circle.filled = False
avgtime /=3
print(avgtime)

plt.subplot(pltrows, pltcols, 3)
plt.imshow(grid, cmap=plt.cm.viridis, alpha=.9, interpolation='nearest')

'''Other strange polygon'''
v = [(10,10), (20,10), (20,20), (80,20), (80,15), (70,15), (70,5), (100,5), (100,90), (70,90), (70,80), (60,80), (60,100), (10,100), (10,10)]
shape = polygon()
shape.set_vertex_list(v)
grid = shape.render_outline()
plt.subplot(pltrows, pltcols, 4)
plt.imshow(grid, cmap=plt.cm.viridis, alpha=.9, interpolation='nearest')
grid = shape.render_filled()
plt.subplot(pltrows, pltcols, 5)
plt.imshow(grid, cmap=plt.cm.viridis, alpha=.9, interpolation='nearest')

""" ax = plt.gca()
# Major ticks
ax.set_xticks(np.arange(0, circle.width, 1))
ax.set_yticks(np.arange(0, circle.height, 1))
# Labels for major ticks
ax.set_xticklabels(np.arange(0, circle.width, 1))
ax.set_yticklabels(np.arange(0, circle.height, 1))
# Minor ticks
ax.set_xticks(np.arange(-.5, circle.width, 1), minor=True)
ax.set_yticks(np.arange(-.5, circle.height, 1), minor=True)
# Gridlines based on minor ticks
ax.grid(which='minor', color='w', linestyle='-', linewidth=1) """

plt.show()