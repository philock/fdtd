import numpy as np
import math
from line import *
from operator import itemgetter

class polygon:
    def __init__(self):
        self.vertices   = []
        self.grid       = None
        self.outlined   = False
        self.filled     = False
        self.x          = 0
        self.y          = 0
        self.width      = 0
        self.height     = 0

    def add_vertex(self, vertex):
        '''Add a Vertex as a tuple (x, y) to the polygon'''
        self.vertices.append(vertex)
        self.determine_surrounding_box()
        self.outlined   = False
        self.filled     = False
    
    def set_vertex_list(self, vertices):
        '''Parameter: list of tuples (x, y) of vertice coordinates'''
        self.vertices = vertices
        self.determine_surrounding_box()
        self.outlined   = False
        self.filled     = False

    #reduces pairs in list to single elements: [2, 5, 5, 8] -> [2, 5, 8]
    def remove_pairs(self):
        results = []
        for item in self.vertices:
            if not(results and item == results[-1]):
                results.append(item)
        self.vertices = results

    def render_outline(self):
        '''returns the outline of the polygon as a binary numpy array. Dimensions are the surrounding box around the polygon.'''
        if self.outlined:
            return self.grid

        self.grid = np.zeros((self.height, self.width))

        for vnum, v in enumerate(self.vertices):

            l = line(v[0], v[1], self.vertices[vnum+1][0], self.vertices[vnum+1][1])

            ys = l.y_box - self.y #starting indices to place the line-box at inside of the local polygon grid
            xs = l.x_box - self.x

            self.grid[ys : ys + l.dy , xs : xs + l.dx] = np.logical_or(self.grid[ys : ys + l.dy , xs : xs + l.dx], l.render())

            if vnum == len(self.vertices)-2:
                break

        self.outlined = True
        self.filled = False
        return self.grid

    def render_filled(self):
        if self.vertices[0] != self.vertices[-1]:
            print("Error: polygon to be filled does not have a closed outline!")
            return

        if self.filled:
            return self.grid
        
        self.remove_pairs() 

        #initialize
        self.grid = np.zeros((self.height, self.width))
        infill = np.zeros_like(self.grid)
        edges = []

        #render outline
        for vnum, v in enumerate(self.vertices):

            l = line(v[0], v[1], self.vertices[vnum+1][0], self.vertices[vnum+1][1])

            ys = l.y_box - self.y #starting indices to place the line-box at inside of the local polygon grid
            xs = l.x_box - self.x

            self.grid[ys : ys + l.dy , xs : xs + l.dx] = np.logical_or(self.grid[ys : ys + l.dy , xs : xs + l.dx], l.render())

            edges.append(l)

            if vnum == len(self.vertices)-2:
                break

        #fill inside
        pixels = np.nonzero(self.grid[1:self.height-1,:])
        for idx in range(0,pixels[0].shape[0]-1):

            x1 = pixels[1][idx]#column indices of an interval between two outline pixels
            x2 = pixels[1][idx + 1]
            y  = pixels[0][idx]#row index inside pixels array, row index inside grid array is y+1

            if y == pixels[0][idx + 1] and x2 != (x1+1):#x1 and x2 need to be in the same row
                if np.any(infill[y, x1:x2]):#if in scanline above there already is some infill in current column interval (x1 x2)
                    infill[y+1, x1+1:x2] = 1
                else:
                    outside = True
                    for l in edges:#test if point is inside of polygon
                        outside = outside ^ self.left_of_line( (x1+1+self.x, y+1+self.y) , l )
                    if not outside:
                        infill[y+1, x1+1:x2] = 1

        
        self.grid = np.logical_or(self.grid, infill)

        self.filled = True
        self.outlined = False

        return self.grid

    def render_vertices(self):
        self.grid = np.zeros((self.height, self.width))

        for v in self.vertices:
            self.grid[v[1]-self.y, v[0]-self.x] = 1

        self.render_filled = False
        self.render_outline = False
        return self.grid

    #tests, weather the given point is left of the line or not. Test done in global grid coordinates
    def left_of_line(self, v, l:line):
        if (v[1] >= l.y_box) and (v[1] < l.y_box + l.dy-1) and (v[0] < l.x_box + l.dx): #check rough boundry box first
            if v[0] < l.x_box:
                return True
            else:
                return np.any(l.grid[v[1] - l.y_box, v[0] - l.x_box + 1 :])
        else:
            return False
            
    def determine_surrounding_box(self):
        '''determines the x and y coordinates of the upper left corner and the width and height of the polygons surrounding box'''
        self.x = min(self.vertices, key = itemgetter(0))[0]
        self.y = min(self.vertices, key = itemgetter(1))[1]
        self.width = max(self.vertices, key = itemgetter(0))[0] - self.x + 1
        self.height = max(self.vertices, key = itemgetter(1))[1] - self.y + 1

        