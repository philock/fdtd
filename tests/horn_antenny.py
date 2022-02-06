""" import sys
sys.path.insert(0,'C:/Users/phili/Programmierung/Python/fdtd/')

print("\n")
print(sys.path)
print("\n") """

import fdtd
import numpy as np
import math
from math import pi

h = 200
w = 400

grid = fdtd.fdtd_grid(w, h, 0.01)


# horn source point
hm = math.ceil(h/2) 
wm = math.ceil(w/2) - 100

# horn shape
opening_radius = 30

# generate horn shape
horn = fdtd.polygon()
horn.set_vertex_list([(wm + 60, hm - opening_radius), (wm + 20, hm - 10), (wm - 5, hm - 10), (wm - 5, hm + 10), (wm + 20, hm + 10), (wm + 60, hm + opening_radius)])
horn.render_outline()


# lens shape
lens_radius = 60
lens_angle  = 90 
yl = math.ceil(h/2) 
xl = math.ceil(w/2) + 10
n_points = 10
point_list = [(xl, yl - lens_radius)]

point_angles = np.linspace(2*pi*lens_angle/360, -2*pi*lens_angle/360, n_points) 

for i in range(n_points):
    x = math.ceil(xl + lens_radius*math.cos(point_angles[i]))
    y = math.ceil(yl + lens_radius*math.sin(point_angles[i]))
    point_list.append((x,y))

point_list.append((xl, yl + lens_radius))
point_list.append((xl, yl - lens_radius))

lens = fdtd.polygon()
lens.set_vertex_list(point_list)
lens.render_filled()

grid.add_object(shape = horn, sigma = 10, rgbv=(1.0, 1.0, 1.0, 1.0))
grid.add_object(shape = lens, er = 1.6)
grid.init_constants()

source = fdtd.fdtd_source((wm, hm), grid, waveform = 'sine', sine_freq = 2e9, type = 'hard')
#source.plot_sine_source(300)

pml_r = fdtd.fdtd_pml(grid, 'right')
pml_l = fdtd.fdtd_pml(grid, 'left')
pml_t = fdtd.fdtd_pml(grid, 'top', width = 25)
pml_b = fdtd.fdtd_pml(grid, 'bottom', width = 25)

sim = fdtd.fdtd_simulation(grid, 1000, 500)
sim.add_source(source)
sim.add_absorber(pml_r)
sim.add_absorber(pml_l)
sim.add_absorber(pml_t)
sim.add_absorber(pml_b)
sim.run()
sim.show_animation(colormap = 'bwr', scale = 'lin', denormalize=False)
#sim.show_animation(colormap = 'plasma', scale = 'log', power = True, denormalize = False, decades = 3, savelocation = r"c://Users/phili/Programmierung/Python/fdtd/videos/horn3.mp4")
#sim.show_animation(colormap = 'bwr', scale = 'lin', power = False, denormalize = False, savelocation = r"c://Users/phili/Programmierung/Python/fdtd/videos/horn1.mp4")
