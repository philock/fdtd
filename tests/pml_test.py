import fdtd

grid = fdtd.fdtd_grid(200, 200, 0.01)
grid.init_constants()


source_shape_v = fdtd.line(100, 50, 100, 150)
source_shape_v.render()
source_v = fdtd.fdtd_source(source_shape_v, grid, ricker_Md=1, ricker_Np=15)

source_shape_h = fdtd.line(50, 100, 150, 100)
source_shape_h.render()
source_h = fdtd.fdtd_source(source_shape_h, grid, ricker_Md=1, ricker_Np=15)

pml_l = fdtd.fdtd_pml(grid, 'left')
pml_r = fdtd.fdtd_pml(grid, 'right')
pml_t = fdtd.fdtd_pml(grid, 'top')
pml_b = fdtd.fdtd_pml(grid, 'bottom')

sim = fdtd.fdtd_simulation(grid, 500, 200)
sim.add_source(source_v)
sim.add_source(source_h)
sim.add_absorber(pml_l)
sim.add_absorber(pml_r)
sim.add_absorber(pml_t)
sim.add_absorber(pml_b)
sim.run()
sim.show_animation(colormap = 'bwr', scale = 'lin')
#sim.show_animation(colormap = 'plasma', scale = 'log', power = True, denormalize = False, decades = 3)