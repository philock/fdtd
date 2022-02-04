import numpy as np
import math

from polygon     import *
from line        import *
from fdtd_object import *

class fdtd_grid:

    '''Constants'''
    c0 = 299792458          # Speed of light
    e0 = 8.8541878128e-12   # Vacuum permittivity
    u0 = 1.25663706212e-6   # Vacuum permeability
    Z0 = 376.730313667      # Free space impedance

    def __init__(self, width, height, delta):
        self.width  = width     # number of grid points in x direction
        self.height = height    # number of grid points in y direction
        self.delta  = delta     # distance between two points (grid spacing)

        self.Hx     = np.zeros((height,      width))   # Magnetic field x component
        self.Hy     = np.zeros((height,      width))   # Magnetic field y component
        self.Ez     = np.zeros((height,      width))   # Electric field z component
        self.er     = np.ones ((height,      width))   # relative permittivity in grid
        self.ur     = np.ones ((height,      width))   # relative permeability in grid
        self.sigma  = np.zeros((height,      width))   # conductivity in grid
        self.sigmam = np.zeros((height,      width))   # magnetic conductivity in grid

        self.Chxh   = np.zeros((height,      width))   # Coefficient for updating Hx from H-field
        self.Chxe   = np.zeros((height,      width))   # Coefficient for updating Hx from E-field

        self.Chyh   = np.zeros((height,      width))   # Coefficient for updating Hy from H-field
        self.Chye   = np.zeros((height,      width))   # Coefficient for updating Hy from E-field

        self.Cezh   = np.zeros((height,      width))   # Coefficient for updating Ez from H-field
        self.Ceze   = np.zeros((height,      width))   # Coefficient for updating Ez from E-field

        self.Cdtds  = 1/math.sqrt(2)                 # Courant number (  =(C0*dt)/dx  )
        self.dt     = self.Cdtds*self.delta/self.c0  # time step

        # list of objects, each object has: 
        # shape:    poly object or line object
        # er:       relative permittivity
        # ur:       relative permeability
        # sigma:    electrical conductivity
        # sigmam:   magnetic conductivity
        # rgbv:     RGB-V color for rendering (4 element tuple)
        self.objects = []                            

    
    def add_object( self, shape, er = 1, ur = 1, sigma = 0, sigmam = 0, rgbv = (0.5, 0.5, 0.5, 0.5)):
        '''Add a object into the grid to simulate. Arguments: shape (line or polygon), 
        relative permittivity, relative permeability, conductivity, magnetic conductivity
        and RGB-V Color for rendering with V as transparency'''
        if er == 0.0 or ur == 0.0:
            raise ValueError('relative permittivity and relative permeability cant be zero!')

        if isinstance(shape, polygon):
            if shape.filled or shape.outlined:
                self.objects.append(fdtd_object(shape, er, ur, sigma, sigmam, rgbv))   

                #Put the rendered polygon inside of the global grid
                mask = np.zeros_like(self.er, dtype = bool)
                mask[shape.y : shape.y + shape.height  ,  shape.x : shape.x + shape.width] = (shape.grid != 0)

                self.er[mask]     = er
                self.ur[mask]     = ur
                self.sigma[mask]  = sigma
                self.sigmam[mask] = sigmam

            else:
                raise ValueError('Polygon is not rendered!')    

        elif isinstance(shape, line):
            if shape.rendered:
                self.objects.append(fdtd_object(shape, er, ur, sigma, sigmam, rgbv))     

                #Put the rendered Line inside of the global grid
                mask = np.zeros_like(self.er, dtype = bool)
                mask[shape.y : shape.y + shape.dy  ,  shape.x : shape.x + shape.dx] = (shape.grid != 0)

                self.er[mask]     = er
                self.ur[mask]     = ur
                self.sigma[mask]  = sigma
                self.sigmam[mask] = sigmam

            else:
                raise ValueError('Line is not rendered!')

        else:
            raise ValueError('Unsupported object type added to Grid! Must be of type Line or Polygon')
        
    def init_constants(self):
        e = self.e0*self.er # permittivity
        u = self.u0*self.ur # permeability

        self.Chxh = (1 - ((self.sigmam * self.dt) / (2 * u))  ) / (  1 + ((self.sigmam * self.dt) / (2 * u))  )

        self.Chxe = ((self.Cdtds/self.ur) / (  1 + ((self.sigmam * self.dt) / (2 * u))  ))

        self.Chyh = (1 - ((self.sigmam * self.dt) / (2 * u))  ) / (  1 + ((self.sigmam * self.dt) / (2 * u))  )

        self.Chye = (self.Cdtds/self.ur) / (  1 + ((self.sigmam * self.dt) / (2 * u))  )

        self.Ceze = (1 - ((self.sigma * self.dt) / (2 * e))  ) / (  1 + ((self.sigma * self.dt) / (2 * e)) )

        self.Cezh = ((self.Cdtds/self.er) / (  1 + ((self.sigma * self.dt) / (2 * e))  ))
        
        return