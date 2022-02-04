from fdtd_simulation import *
from fdtd_grid import *
from fdtd_pml import *

grid = fdtd_grid(200, 200, 0.01)
grid.init_constants()


source_shape = line(100, 50, 100, 150)
source_shape.render()
source = fdtd_source(source_shape, grid, ricker_Md=1, ricker_Np=15)

pml = fdtd_pml(grid, 'right')

sim = fdtd_simulation(grid, 500, 200)
sim.add_source(source)
sim.add_absorber(pml)
sim.run()
#sim.show_animation(colormap = 'bwr', scale = 'lin')
sim.show_animation(colormap = 'plasma', scale = 'log', power = True, denormalize = False, decades = 3)