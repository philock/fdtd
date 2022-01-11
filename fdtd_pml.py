import  numpy as np
import  math
from    fdtd_grid import *

class fdtd_pml():
    def __init__(self, grid : fdtd_grid, pos, width = 10, sigma_max = 40, a = 1.0e-8):
        self.width  = width
        self.grid   = grid

        #quadratic increasing profile of conductivity, from 0 up to sigma_max. shape = (1, width)
        sigma_curve = sigma_max*np.linspace(0.0, 1.0, width)**2

        #constants vectors. shape = (1, width)
        self.be     = np.exp(-(a/grid.e0 + sigma_curve/grid.e0)*grid.dt)
        self.bh     = np.exp(-(a/grid.u0 + sigma_curve/grid.u0)*grid.dt)
        self.ce     = (self.be - 1)*sigma_curve/(sigma_curve + a)
        self.ch     = (self.be - 1)*sigma_curve/(sigma_curve + a)

        match pos:
            case 'right':
                self.psi_ez = np.zeros((grid.height, grid.width, 2))
                self.psi_hx = np.zeros((grid.height-1, grid.width))
                self.psi_hy = np.zeros((grid.height, grid.width - 1))

                #self.region_ez = (slice(1, -1), slice(grid.width - width - 1, -1))
                #self.region_hx = (slice(1, -1), slice(grid.width - width - 1, -1))
                #self.region_hy = (slice(1, -1), slice(grid.width - width - 1, -1))
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
        st = self.grid.width - self.width - 1

        self.psi_ez[:, st:-1, 0] *= self.be
        self.psi_ez[:, st:-1, 1] *= self.be

        Hy = self.grid.Hy
        Hx = self.grid.Hx

        self.psi_ez[1:-1,st:-1] += (Hy[1:-1,st:] - Hy[1:-1,st-1:-1]) * self.ce
        self.psi_ez[1:-1,st:-1] += (Hx[1:,st:-1] - Hx[:-1,st:-1]) * self.ce
    
    def update_H(self):
        st = self.grid.width - self.width - 1
        sty = st + 1

        self.psi_hx[:,st:] *= self.bh
        self.psi_hy[:,sty:] *= self.bh

        Ez = self.grid.Ez

        self.psi_hx[:, st:] += (Ez[1:,st:]-Ez[:-1,st:])*self.ce
        self.psi_hy[:, sty:] += (Ez[:,st+1:]-Ez[:,st:-1])*self.ce

    def apply_E(self):
        st = self.grid.width - self.width - 1
        self.grid.Ez[1:-1,st:-1] += (self.psi_ez[:,:,0] - self.psi_ez[:,:,1]) * (1/self.grid.e0) * self.grid.Cdtds
        #self.grid.Ez[self.region_ez] += (self.psi_ez[:,:,0] - self.psi_ez[:,:,1]) * self.grid.Cdtds

    def apply_H(self):
        st = self.grid.width - self.width - 1
        sty = st - 1
        self.grid.Hx[:, st:] -= self.psi_hx[:,:] * (1/self.grid.u0) * self.grid.Cdtds
        self.grid.Hy[:, sty:] += self.psi_hy[:,:] * (1/self.grid.u0) * self.grid.Cdtds
        #self.grid.Hx[self.region_hx] -= self.psi_hx[:,:] *  self.grid.Cdtds
        #self.grid.Hy[self.region_hy] += self.psi_hy[:,:] *  self.grid.Cdtds
