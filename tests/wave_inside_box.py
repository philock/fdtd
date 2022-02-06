import fdtd
import numpy as np

grid = fdtd.fdtd_grid(200, 200, 0.01)

box = fdtd.polygon()
box.set_vertex_list([(50, 50), (50, 150), (150, 150), (150, 50), (50, 50)])
box.render_outline()

grid.add_object(shape = box, sigma = 10)
grid.init_constants()

source_shape = fdtd.line(95, 100, 105, 100)
source_shape.render()
source = fdtd.fdtd_source(source_shape, grid, type = 'soft')
#source.plot_ricker_source(200)

sim = fdtd.fdtd_simulation(grid, 100, 100)
sim.add_source(source)
sim.run()
print(np.max(sim.snapshots))
print(np.min(sim.snapshots))
sim.show_animation(colormap = 'bwr', scale = 'lin', decades = 15, denormalize=False)