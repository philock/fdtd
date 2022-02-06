import fdtd
from math import ceil
import numpy as np
import matplotlib.pyplot as plt

w = 250
h = 200

grid = fdtd.fdtd_grid(w, h, 0.01)

# mirror position
mx = ceil(w/2) + 60
my = ceil(h/2)
# mirror width
mw = 60
# mirror curvature
mc = 0.005

m_y_p = np.arange(-mw, mw + 1, 1, dtype='int')
m_x_p = mc*m_y_p**2
m_x_p = np.ceil(m_x_p)
m_x_p = m_x_p.astype(int)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(m_y_p,m_x_p)
ax.set_aspect('equal', adjustable='box')
plt.show()

mirror_shape = []
mirror = fdtd.polygon()
for i in range(np.size(m_y_p)):
    mirror_shape.append((mx - m_x_p[i], my + m_y_p[i]))

mirror.set_vertex_list(mirror_shape)
mirror.render_outline()
grid.add_object(mirror, sigma = 10, rgbv = (1.0, 1.0, 1.0, 1.0))
grid.init_constants()

sx = ceil(w/2) - 60
source_shape = fdtd.line(sx, 40, sx, h - 40)
source_shape.render()
#source = fdtd.fdtd_source(source_shape, grid, waveform='sine', sine_freq = 3e9)
source = fdtd.fdtd_source(source_shape, grid, ricker_Np = 15)

pml_l = fdtd.fdtd_pml(grid, 'left', width = 60)
pml_r = fdtd.fdtd_pml(grid, 'right')
pml_t = fdtd.fdtd_pml(grid, 'top', width = 25)
pml_b = fdtd.fdtd_pml(grid, 'bottom', width = 25)

sim = fdtd.fdtd_simulation(grid, 500, 250)
sim.add_source(source)
sim.add_absorber(pml_l)
sim.add_absorber(pml_r)
sim.add_absorber(pml_t)
sim.add_absorber(pml_b)
sim.run()
sim.show_animation(colormap = 'bwr', scale = 'lin', denormalize=False)
#sim.show_animation(colormap = 'plasma', scale = 'log', power = True, denormalize = False, decades = 3)

