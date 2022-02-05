import numpy as np
from operator import itemgetter
from fdtd import line
import matplotlib.pyplot as plt

def left_of_line(v, l:line):
    if (v[1] >= l.y_box) and (v[1] < l.y_box + l.dy-1) and (v[0] < l.x_box + l.dx): #check rough boundry box first
        if v[0] < l.x_box:
            return True
        else:
            return np.any(l.grid[v[1] - l.y_box, v[0] - l.x_box + 1 :])
    else:
        return False


#vertices = [(0,0), (10,0), (10,10), (5,10), (5,3), (0,3), (0,0)]
vertices = [(10,10), (20,10), (20,20), (80,20), (80,15), (70,15), (70,5), (100,5), (100,90), (70,90), (70,80), (60,80), (60,100), (10,100), (10,10)]
edges = []

#render outline
for vnum, v in enumerate(vertices):

    l = line(v[0], v[1], vertices[vnum+1][0], vertices[vnum+1][1])
    l.render()

    edges.append(l)

    if vnum == len(vertices)-2:
        break


outside = True
for l in edges:#test if point is inside of polygon
    x = left_of_line( (61,90) , l)
    print(x)
    outside = outside ^ x
print(outside)