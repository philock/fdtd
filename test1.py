import numpy as np
import matplotlib.pyplot as plt

thickness = 10
Ny = 200
Nz = 200

def _sigma(vect):
    """ create a cubicly increasing profile for the conductivity """
    return 40 * vect ** 3 / (thickness + 1) ** 4

def _set_sigmaE():
    sigma = _sigma(np.arange(0.5, thickness + 0.5, 1.0))
    sigmaE = np.zeros((thickness, Ny, Nz, 3))
    sigmaE[:, :, :, 0] = sigma[:, None, None]
    print(sigmaE[:, 0, 0, 0])

_set_sigmaE()