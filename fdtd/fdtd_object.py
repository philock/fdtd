class fdtd_object:
    def __init__(self, shape, er, ur, sigma, sigmam, rgbv):
        self.shape  = shape
        self.er     = er
        self.ur     = ur
        self.sigma  = sigma
        self.sigmam = sigmam
        self.rgbv   = rgbv