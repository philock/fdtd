import numpy as np
import math

class line:

    def __init__(self, xa, ya, xb, yb):
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

        self.dx = abs(xb-xa)+1#number of columns of returned render
        self.dy = abs(yb-ya)+1#number of rows of returned render

        #indices of upper left corner of box surrounding the line
        self.y_box = ya
        self.x_box = xa
        if xb<xa:
            self.x_box = xa - self.dx + 1
        if yb<ya:
            self.y_box = ya - self.dy + 1

        #Flags for horizontal or vertical Lines
        self.vline = False
        self.hline = False
        if xa == xb:
            self.vline = True
        if ya == yb:
            self.hline = True


        self.grid = np.zeros((self.dy, self.dx))
        self.rendered = False

    def length(self):
        return math.sqrt((self.xa-self.xb)**2 + (self.ya-self.yb)**2)

    def render(self):
        '''
        returns numpy array with dimensions of surrounding box of line.
        '''
        
        m =  abs(self.dx/self.dy)
        
        if m>1:
            m = 1/m
            for i in range(self.dx):
                self.grid[math.floor(i*m), i] = 1
        else:
            for i in range(self.dy):
                self.grid[i, math.floor(i*m)] = 1

        if self.xb<self.xa:
            self.grid = np.fliplr(self.grid)

        if self.yb<self.ya:
            self.grid = np.flipud(self.grid)

        self.rendered = True
        return self.grid