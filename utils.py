import numpy as np

class Config():

    def __init__(self, X, x, Q, Y, y, noise):
        self.X = X
        self.x = x
        self.Q = Q
        self.Y = Y
        self.y = y
        self.noise = noise

    def get_configurations(self):
        return list(vars(self).values())

def get_amplitude(point):
    real, imag = point.real, point.imag
    amplitude = np.sqrt((real ** 2) + (imag ** 2))
    return np.abs(point)
    return amplitude

def get_phase(point):
    real, imag = point.real, point.imag
    # phase = np.arctan2(imag, real)
    # phase = np.arctan(imag / real)
    phase = np.angle(point)
    return phase

get_amplitude_vectorized = np.vectorize(get_amplitude, otypes=[float])
get_phase_vectorized = np.vectorize(get_phase, otypes=[float])

def cart_to_pol(spectrum):
    return np.abs(spectrum), np.angle(spectrum)
    return get_amplitude_vectorized(spectrum), get_phase_vectorized(spectrum)

def combine_to_complex(real, imag):
    return complex(real, imag)

combine_to_complex_vectorized = np.vectorize(combine_to_complex, otypes=[complex])

def pol_to_cart(amplitude, phase):
    return combine_to_complex_vectorized(amplitude * np.cos(phase), amplitude * np.sin(phase))


PRESET_1 = {
    'X': 1,
    'x': 0,
    'Q': 0,
    'Y': 1,
    'y': 0,
    'noise': 0
}

PRESET_2 = {
    'X': 0,
    'x': 1,
    'Q': 0,
    'Y': 0,
    'y': 1,
    'noise': 0
}

PRESET_3 = {
    'X': 0,
    'x': 1,
    'Q': 0,
    'Y': 1,
    'y': 0,
    'noise': 0
}

PRESET_4 = {
    'X': 0,
    'x': 0,
    'Q': 1
}

SOUND_1 = Config(1, 0, 0, 1, 0, 0)
SOUND_2 = Config(0, 1, 0, 0, 1, 0)
HYBRID_1 = Config(0, 1, 0, 1, 0, 0)
HYBRID_2 = Config(0, 0, 1, 1, 0, 0.2)
