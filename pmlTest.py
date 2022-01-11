from fdtd_simulation import *
from fdtd_grid import *
from fdtd_pml import *

grid = fdtd_grid(200, 200, 0.01)
grid.init_constants()


source_shape = line(50, 50, 50, 150)
source_shape.render()
source = fdtd_source(source_shape, grid)

pml = fdtd_pml(grid, 'right')

sim = fdtd_simulation(grid, 200, 200)
sim.add_source(source)
sim.add_absorber(pml)
sim.run()
sim.show_animation(colormap = 'bwr', scale = 'symlog', power = False, decades = 4)