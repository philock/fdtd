from .fdtd_grid  import fdtd_grid
from .line       import line
from .polygon    import polygon
from math       import pi, sin, exp
import matplotlib.pyplot as plt
import numpy as np

class fdtd_source():

    # Often used source functions
    def ricker_wavelet_func(self, i):
        a = self.rw_ScNp * i - self.rw_Md
        a = pi*pi*a*a 
        return self.amplitude*(1 - 2*a)*exp(-1*a)

    def sine_func(self, i):
        return self.amplitude*sin(self.omega*i)

    def step_func(self, i):
        if i >= self.step_start and i < self.step_stop:
            return self.amplitude
        else: 
            return 0.0

    def __init__(self, 
                shape,                              # shape of source. Can be line object, polygon object or tuple
                grid      : fdtd_grid = None,       # grid on which the source should be applied. This is only to generate the shape mask of correct size and obtain time step size
                type      = 'soft',                 # soft source is additive to grid value, hard source overwrites grid value
                waveform  = 'ricker',               # type of waveform of source. Can be ricker, sine, step or arb
                ricker_Md = 1,   ricker_Np = 20,    # parameters for ricker source. Np: number of points per wavelength, Md: delay multiple
                step_start= None, step_stop = None, # parameters for step function: time step of turn on and time step of turn off
                sine_freq = None,                   # parameter for sine function: frequency
                arb_func  = None,                   # parameter for arb source: function of signature f(i)            
                amplitude = 1.0):                   # multiplicative amplitude for all source types

        self.type       = type
        self.shape      = shape
        self.amplitude  = amplitude

        self.waveform   = waveform

        #ricker wavelet parameters
        self.rw_Md      = ricker_Md
        self.rw_Np      = ricker_Np

        #step function parameters
        self.step_start = step_start
        self.step_stop  = step_stop

        #sine function parameter
        self.sine_freq  = sine_freq
    
        self.mask          = None
        self.wavefrom_func = None

        #set waveform function to use in apply() and derive constants for waveform specified
        if waveform == 'ricker':
            if ricker_Md is None or ricker_Np is None or grid is None: raise ValueError('ricker_Md, ricker_Np and grid need to be specified for ricker wavelet!')

            self.waveform_func = self.ricker_wavelet_func
            self.rw_ScNp = grid.Cdtds/ricker_Np
        elif waveform == 'sine':
            if sine_freq is None: raise ValueError('sine_freq need to be specified for sine function!')
            self.waveform_func = self.sine_func

            self.omega = 2*pi*sine_freq*grid.dt
        elif waveform == 'step':
            if step_start is None or step_stop is None: raise ValueError('step_start and step_stop need to be specified for step function!')
            self.waveform_func = self.step_func
        elif waveform == 'arb':
            if arb_func is None: raise ValueError('arb_func needs to be supplied for arbitary source! Needs parameter i for time step')
            self.waveform_func = arb_func
        else:
            raise ValueError('Unknown source waveform! Should be ricker, sine, step or arb!')

        #generate mask for the area of the grid the source should be applied on
        if isinstance(shape, line):
            if not shape.rendered:
                raise ValueError('Line defining source shape is not rendered!')

            self.mask = np.zeros_like(grid.Ez, dtype = bool)
            self.mask[shape.y_box : shape.y_box + shape.dy  ,  shape.x_box : shape.x_box + shape.dx] = (shape.grid != 0)
        elif isinstance(shape, polygon):
            if not (shape.filled or shape.outlined):
                raise ValueError('Polygon defining source shape is not rendered!')

            self.mask = np.zeros_like(grid.Ez, dtype = bool)
            self.mask[shape.y : shape.y + shape.height  ,  shape.x : shape.x + shape.width] = (shape.grid != 0)
        elif isinstance(shape, tuple):
            mask = None
        else: 
            raise ValueError('Unknown source shape! Should be line object, polygon object or tuple for point source!')

    def apply(self, grid : fdtd_grid, i):

        if self.mask is None: # Point source 

            if self.type == 'soft':
                grid.Ez[self.shape[1], self.shape[0]] = grid.Ez[self.shape[1], self.shape[0]] + self.waveform_func(i)
            else: # hard source
                grid.Ez[self.shape[1], self.shape[0]] = self.waveform_func(i)
        else: # Line or Polygon-shaped source
            if self.type == 'soft':
                grid.Ez[self.mask] = grid.Ez[self.mask] + self.waveform_func(i)
            else: # hard source
                grid.Ez[self.mask] = self.waveform_func(i)

    def plot_ricker_source(self, n):
        x = np.zeros(n)
        for i in range(n):
            x[i] = self.ricker_wavelet_func(i)

        plt.plot(x)
        plt.show()

    def plot_sine_source(self, n):
        x = np.zeros(n)
        for i in range(n):
            x[i] = self.sine_func(i)

        plt.plot(x)
        plt.show()

