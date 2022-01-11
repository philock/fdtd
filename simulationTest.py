from fdtd_simulation import *
from fdtd_grid import *

w = 450
h = 450

i = 300
j = 420
a = (i,i)
b = (j,i)
c = (j,j)
d = (i,j)
square = polygon()
square.set_vertex_list([a,b,c,d,a])
square.render_filled()

a = 100
b = 200 
triangle = polygon()
triangle.set_vertex_list([(a,a), (a,b), (b, b), (a,a)])
triangle.render_filled()

grid = fdtd_grid(w, h, 0.01)
grid.add_object(square,   er = 1.3, sigma = 50, rgbv= (0.0, 0.9, 0.0, 0.9))
grid.add_object(triangle, er = 3, sigma = 30, rgbv=   (0.0, 0.0, 0.8, 0.9))
grid.init_constants()

source_line_shape = line(200, 230, 200, 290)
source_line_shape.render()
line_source = fdtd_source(shape = triangle, grid = grid, type = 'soft', ricker_Md = 1, ricker_Np = 20) # default source: ricker wavelet
#line_source.plot_ricker_source(500)

sim = fdtd_simulation(grid, 1000, 200)
sim.add_source(line_source)
sim.run()
#sim.show_individual(10)
#sim.show_animation(savelocation = r"c://Users/phili/Programmierung/Python/fdtd/videos/test7.mp4", frameinterval = 100, colormap = 'inferno', scale = 'log', power = True, decades = 4)
sim.show_animation(colormap = 'inferno', scale = 'log', power = True, decades = 4)

