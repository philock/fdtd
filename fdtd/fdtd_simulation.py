import math 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as clr

from .fdtd_grid import fdtd_grid
from .fdtd_source import fdtd_source
from .fdtd_pml    import fdtd_pml

class fdtd_simulation():
    def __init__(self, grid: fdtd_grid, Nsteps, Nsnaps):
        self.grid       = grid
        self.Nsteps     = Nsteps
        self.Nsnaps     = Nsnaps
        self.snapshots  = np.zeros((grid.height, grid.width, Nsnaps)) 
        
        self.sources    : fdtd_source = [] 
        self.absorbers  : fdtd_pml    = []

    def run(self):
        if not self.grid.constants_initialized: raise ValueError("Constants of grid have not been initialized! Run grid.init_constants() after adding all objects!")

        dsn = math.ceil(self.Nsteps/self.Nsnaps) # distance in steps between two snapshots

        for s in range(self.Nsteps):

            
            #update H-fields in PML
            for a in self.absorbers:
                a.update_H()

            # update H field
            self.grid.Hx[:-1,:] = self.grid.Chxh[:-1,:] * self.grid.Hx[:-1,:] - self.grid.Chxe[:-1,:] * (self.grid.Ez[1:,:] - self.grid.Ez[:-1,:])
            self.grid.Hy[:,:-1] = self.grid.Chyh[:,:-1] * self.grid.Hy[:,:-1] + self.grid.Chye[:,:-1] * (self.grid.Ez[:,1:] - self.grid.Ez[:,:-1])

            #apply PML to H-field
            for a in self.absorbers:
                a.apply_H()

            #update E-fields in PML
            for a in self.absorbers:
                a.update_E()

            # update E field
            #self.grid.Ez[1:-1,1:-1] = self.grid.Ceze[1:-1,1:-1] * self.grid.Ez[1:-1,1:-1] + self.grid.Cezh[1:-1,1:-1] * ((self.grid.Hy[1:-1,1:-1] - self.grid.Hy[1:-1,:-2]) - (self.grid.Hx[1:-1,1:-1] - self.grid.Hx[:-2,1:-1]))
            self.grid.Ez[1:,1:] = self.grid.Ceze[1:,1:] * self.grid.Ez[1:,1:] + self.grid.Cezh[1:,1:] * ((self.grid.Hy[1:,1:] - self.grid.Hy[1:,:-1]) - (self.grid.Hx[1:,1:] - self.grid.Hx[:-1,1:]))

            #apply PML to E-field
            for a in self.absorbers:
                a.apply_E()
                
            # Apply sources
            for src in self.sources:
                src.apply(self.grid, s)

            # take Ez-field snapshot
            if s%dsn == 0:
                self.snapshots[:,:,math.floor(s/dsn)] = self.grid.Ez

            print(100*s/self.Nsteps,'%')

    def show_individual(self, Nshow = 'all'):
        '''Shows each snapshot as an individual plot inside one window. 
            Parameter Nshow determines up to wich snapshot is to be displayed. 
            If left empty (default), all snapshots get displayed. 
            Maximal number of snapshots to show is 50'''

        if Nshow == 'all':
            if self.Nsnaps > 50:
                raise ValueError('Too many snapshots to show in one image!')
            
            Nplots_xy = math.ceil(math.sqrt(self.Nsnaps))
            cnorm = plt.Normalize(-1, 1, clip = True)

            for i in range(self.Nsnaps):
                plt.subplot(Nplots_xy, Nplots_xy, i+1)
                plt.imshow(self.log_color(self.snapshots[:,:,i], 1), cmap='plasma', vmin = -3, vmax = 0)
                plt.colorbar()

        else:
            if Nshow > 50:
                raise ValueError('Too many snapshots to show in one image!')
            
            Nplots_xy = math.ceil(math.sqrt(Nshow))
            for i in range(Nshow):
                plt.subplot(Nplots_xy, Nplots_xy, i+1)
                plt.imshow(self.snapshots[:,:,i], cmap='hot')

        plt.show()

    def show_animation(self, savelocation = None, colormap = None, power = False, scale = 'lin', decades = 4, denormalize = True, frameinterval = 30):
        '''Shows animation of Electric field together with simulation objects. Visualization options:
            Power of field or raw electric field (default)
            'log': Logarithmic plot (default):
                Absoulute value of field gets plotted on a Log10 scale, relative to maximal value of Power or raw field 
                Specify number of decades to plot, default is 4 decaded (down to -10^-4 dB)
            'symlog': Symetrical logarithmic plot:
                Field gets plotted with log10-scale in both positive and negative direction
                Specify number of decades to plot logarithmic, after that the plot will continue linear 
            'lin': Linear plot:
                Field gets plotted with linear scale
            denormalize field with sqrt(e0) (default). This leads to much smaller values. Alternatively the normalized field can be plotted'''        

        if denormalize: 
            self.snapshots = math.sqrt(self.grid.e0)*self.snapshots

        if power:
            self.snapshots = np.power(self.snapshots, 2)
        
        if scale == 'log':
            max = np.max(self.snapshots)
            norm = clr.LogNorm(vmax = max, vmin = pow(10, (-1*decades) ), clip = True )
        elif scale == 'symlog':
            max = np.max(self.snapshots)
            norm = clr.SymLogNorm(linthresh = pow(10, (-1*decades) ), vmax = max, vmin = -max, base = 10)

            """ norm = clr.NoNorm()
            max = np.max(self.snapshots)
            min = np.min(self.snapshots)
            pos = self.snapshots >= pow(10, -decades)
            neg = self.snapshots <= -pow(10, -decades)
            self.snapshots[np.abs(self.snapshots) < pow(10, -decades)] = 0.5 + self.snapshots[np.abs(self.snapshots) < pow(10, -decades)]
            self.snapshots[pos] = np.interp(np.log10(self.snapshots[pos]), (-decades, np.log10(max)), (0.5, 1.0))
            self.snapshots[neg] = np.interp(np.log10(np.abs(self.snapshots[neg])), (-decades, np.log10(np.abs(min))), (0.5, 0.0))"""
        elif scale == 'lin':
            if power:
                norm = clr.Normalize(vmin = np.min(self.snapshots), vmax = np.max(self.snapshots) )
            else:
                norm = clr.TwoSlopeNorm(vcenter = 0.0, vmin = np.min(self.snapshots), vmax = np.max(self.snapshots) )
        else:
            raise ValueError('unknown scale! Use log, symlog or lin')
     
        fig     = plt.figure()
        im      = plt.imshow(self.snapshots[:,:,0], norm = norm, cmap=colormap)
        self.overlay_objects()

        def update(i):
            im.set_data(self.snapshots[:,:,i])
            return [im]

        anim = animation.FuncAnimation(fig, update, frames = self.Nsnaps, interval = frameinterval)

        if savelocation:
            writervideo = animation.FFMpegWriter( fps=math.floor(1000 / frameinterval) ) 
            plt.rcParams['animation.ffmpeg_path'] = r'C://Users/phili/Programmierung/Python/fdtd/ffmpeg-4.4.1-essentials_build/bin/ffmpeg.exe'
            print('Writing video file...')
            anim.save(savelocation, writer = writervideo)

        plt.show()

    def add_source(self, source : fdtd_source):
        self.sources.append(source)

    def add_absorber(self, absorber):
        self.absorbers.append(absorber)

    def overlay_objects(self):
        for o in self.grid.objects:

            mask = np.zeros_like(self.grid.Ez, dtype = bool)
            mask[o.shape.y : o.shape.y + o.shape.height  ,  o.shape.x : o.shape.x + o.shape.width] = (o.shape.grid != 0)

            img = np.zeros((self.grid.height, self.grid.width, 4)) # image with r,g,b and v channel
            img[mask, 0] = o.rgbv[0] # red
            img[mask, 1] = o.rgbv[1] # green
            img[mask, 2] = o.rgbv[2] # blue
            img[mask, 3] = o.rgbv[3] # transparency
            plt.imshow(img)

        for a in self.absorbers:
            match a.position:
                case 'right':
                    plt.axvline(self.grid.width - a.width)
                case 'left':
                    plt.axvline(a.width)
                case 'top':
                    plt.axhline(a.width)
                case 'bottom':
                    plt.axhline(self.grid.height - a.width)
                case _:
                    pass

    def log_color(self, data, normalize):
        return np.log10((np.power( np.abs(data)+ 1e-9, 2)) / normalize)