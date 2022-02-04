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

        plt.plot(sigma_curve)
        plt.show(block = True)

        #constants vectors. shape = (1, width)
        self.be = np.exp(-(a + sigma_curve) * grid.Cdtds)
        self.ce = ((self.be - 1.0)* sigma_curve / (sigma_curve + a))

        self.bh = np.exp(-(a + sigma_curve) * grid.Cdtds)
        self.ch = ((self.bh - 1.0)* sigma_curve/ (sigma_curve + a))

        self.psi_ez = np.zeros((grid.height, grid.width, 2))
        self.psi_hx = np.zeros((grid.height, grid.width))
        self.psi_hy = np.zeros((grid.height, grid.width))

        match pos:
            case 'right':
                self.region = (slice(None), slice(-grid.width, None))
                self.region_hx = (slice(1, -1), slice(grid.width - width - 1, -1))
                self.region_hy = (slice(1, -1), slice(grid.width - width - 1, -1))
            case 'left':
                self.be = np.flip(self.be)
                self.bh = np.flip(self.bh)
                self.ce = np.flip(self.ce)
                self.ch = np.flip(self.ch)
                pass
            case 'top':
                pass
            case 'bottom':
                pass
            case _:
                raise ValueError("Unknown position of PML! Use 'right', 'left', 'top' or 'bottom'.")
    
    def update_E(self):
        st = -self.width

        self.psi_ez[:, st:, 0] *= self.be
        self.psi_ez[:, st:, 1] *= self.be

        Hy = self.grid.Hy
        Hx = self.grid.Hx

        self.psi_ez[:,  st+1:, 0] += (Hy[:,st+1:] - Hy[:,st:-1]) * self.ce[1:]
        self.psi_ez[1:, st:, 1] += (Hx[1:,st:] - Hx[:-1,st:]) * 0#self.ce
    
    def update_H(self):
        st = -self.width

        self.psi_hx[:,st:] *= self.bh
        self.psi_hy[:,st:] *= self.bh

        Ez = self.grid.Ez

        self.psi_hx[:-1, st:] += (Ez[1:,st:]-Ez[:-1,st:])*0#self.ce
        self.psi_hy[:,   st:-1] += (Ez[:,st+1:]-Ez[:,st:-1])*self.ce[:-1]

    def apply_E(self):
        self.grid.Ez += (self.psi_ez[:,:,0] - self.psi_ez[:,:,1]) * self.grid.Cdtds

    def apply_H(self):
        self.grid.Hx += self.psi_hx[:,:] * self.grid.Cdtds
        self.grid.Hy -= self.psi_hy[:,:] * self.grid.Cdtds