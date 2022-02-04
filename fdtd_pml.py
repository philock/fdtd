import  numpy as np
import  math
from    fdtd_grid import *
import matplotlib.pyplot as plt

class fdtd_pml():
    def __init__(self, grid : fdtd_grid, pos, width = 45, sigma_max = 3, a = 1.0e-8):
        self.width    = width
        self.grid     = grid
        self.position = pos

        #qubic increasing profile of conductivity, from 0 up to sigma_max. shape = (1, width)
        sigma_curve = sigma_max * np.linspace(0.0, 1.0, width)**3

        #plt.plot(sigma_curve)
        #plt.show(block = True)

        self.psi_ez_y = np.zeros((grid.height, grid.width))
        self.psi_ez_x = np.zeros((grid.height, grid.width))
        self.psi_hx = np.zeros((grid.height, grid.width))
        self.psi_hy = np.zeros((grid.height, grid.width))

        #constants vectors. shape = (1, width)
        self.be = np.exp(-(a + sigma_curve) * grid.Cdtds)
        self.bh = np.exp(-(a + sigma_curve) * grid.Cdtds)

        match pos:
            case 'right':
                self.region = (slice(None), slice(-self.width, None))

                #absorbing conductivity only in x-direction
                self.ce_x = ((self.be - 1.0)* sigma_curve / (sigma_curve + a))
                self.ce_y = np.zeros(grid.height)
                self.ch_x = ((self.bh - 1.0)* sigma_curve/ (sigma_curve + a))
                self.ch_y = np.zeros(grid.height)

                #Turn into column vectors for element wise multiplication.
                self.ce_y = self.ce_y[:, None]
                self.ch_y = self.ch_y[:, None]
            case 'left':
                self.region = (slice(None), slice(None, self.width))

                #conductivity profile rising into the negative x-direction
                sigma_curve = np.flip(sigma_curve)
                self.be = np.flip(self.be)
                self.bh = np.flip(self.bh)
                
                #absorbing conductivity only in x-direction
                self.ce_x = ((self.be - 1.0)* sigma_curve / (sigma_curve + a))
                self.ce_y = np.zeros(grid.height)
                self.ch_x = ((self.bh - 1.0)* sigma_curve/ (sigma_curve + a))
                self.ch_y = np.zeros(grid.height)

                #Turn into column vectors for element wise multiplication.
                self.ce_y = self.ce_y[:, None]
                self.ch_y = self.ch_y[:, None]
                pass
            case 'top':
                self.region = (slice(None, self.width), slice(None))

                #conductivity profile rising into the positive y-direction
                sigma_curve = np.flip(sigma_curve)
                self.be = np.flip(self.be)
                self.bh = np.flip(self.bh)
                
                #absorbing conductivity only in x-direction
                self.ce_x = np.zeros(grid.width)
                self.ce_y = ((self.be - 1.0)* sigma_curve / (sigma_curve + a))
                self.ch_x = np.zeros(grid.width)
                self.ch_y = ((self.bh - 1.0)* sigma_curve/ (sigma_curve + a))

                #Turn into column vectors for element wise multiplication.
                self.ce_y = self.ce_y[:, None]
                self.ch_y = self.ch_y[:, None]
                self.be   = self.be[:, None]
                self.bh   = self.bh[:, None]
            case 'bottom':
                self.region = (slice(-self.width, None), slice(None))
                
                #absorbing conductivity only in x-direction
                self.ce_x = np.zeros(grid.width)
                self.ce_y = ((self.be - 1.0)* sigma_curve / (sigma_curve + a))
                self.ch_x = np.zeros(grid.width)
                self.ch_y = ((self.bh - 1.0)* sigma_curve/ (sigma_curve + a))

                #Turn into column vectors for element wise multiplication.
                self.ce_y = self.ce_y[:, None]
                self.ch_y = self.ch_y[:, None]
                self.be   = self.be[:, None]
                self.bh   = self.bh[:, None]
            case _:
                raise ValueError("Unknown position of PML! Use 'right', 'left', 'top' or 'bottom'.")
    
    def update_E(self):
        self.psi_ez_x[self.region] *= self.be
        self.psi_ez_y[self.region] *= self.be

        Hy = self.grid.Hy[self.region]
        Hx = self.grid.Hx[self.region]
        psi_ez_x = self.psi_ez_x[self.region]
        psi_ez_y = self.psi_ez_y[self.region]

        psi_ez_x[:, 1:] += (Hy[:,1:] - Hy[:,:-1]) * self.ce_x[1:]
        psi_ez_y[1:, :] += (Hx[1:,:] - Hx[:-1,:]) * self.ce_y[1:]
    
    def update_H(self):
        self.psi_hx[self.region] *= self.bh
        self.psi_hy[self.region] *= self.bh

        Ez = self.grid.Ez[self.region]
        psi_hx = self.psi_hx[self.region]
        psi_hy = self.psi_hy[self.region]

        psi_hx[:-1, :] += (Ez[1:,:]-Ez[:-1,:])*self.ch_y[:-1]
        psi_hy[:,   :-1] += (Ez[:,1:]-Ez[:,:-1])*self.ch_x[:-1]

    def apply_E(self):
        self.grid.Ez += (self.psi_ez_x[:,:] - self.psi_ez_y[:,:]) * self.grid.Cdtds

    def apply_H(self):
        self.grid.Hx += self.psi_hx[:,:] * self.grid.Cdtds
        self.grid.Hy -= self.psi_hy[:,:] * self.grid.Cdtds