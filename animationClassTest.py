import random
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation

class animationClassTest():
    def anitest(self):
        fps = 2
        nSeconds = 2
        #snapshots = [ np.random.rand(10,10) for _ in range( nSeconds * fps ) ]
        snapshots = np.random.rand(10,10,nSeconds*fps)
        snapshots[:,:,1:] = snapshots[:,:,1:]*0.00001
        

        fig  = plt.figure()
        im   = plt.imshow(snapshots[:,:,0], cmap='hot')

        def animate_func(i):
            im.set_array(snapshots[:,:,i])
            return [im]

        anim = animation.FuncAnimation(
                                    fig, 
                                    animate_func, 
                                    frames = 4,
                                    interval = 200, # in ms
                                    )

        plt.show() 
