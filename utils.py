import numpy as np
import os

class Config():

    def __init__(self, X, x, Q, Y, y, noise_threshold):
        self.X = X
        self.x = x
        self.Q = Q
        self.Y = Y
        self.y = y
        self.noise_threshold = noise_threshold

    def get_configurations(self):
        return list(vars(self).values())

def cart_to_pol(spectrum):
    return np.abs(spectrum), np.angle(spectrum)
    # return get_amplitude_vectorized(spectrum), get_phase_vectorized(spectrum) # DEPRECATED

def combine_to_complex(real, imag):
    return complex(real, imag)

combine_to_complex_vectorized = np.vectorize(combine_to_complex, otypes=[complex])

def pol_to_cart(amplitude, phase):
    return combine_to_complex_vectorized(amplitude * np.cos(phase), amplitude * np.sin(phase))

def filter_noise(spectrum, noise_threshold):
    return np.vectorize(lambda val: val if val > noise_threshold else 0., otypes=[float])(spectrum)

SOUND_1 = Config(1, 0, 0, 1, 0, 0)
SOUND_2 = Config(0, 1, 0, 0, 1, 0)
HYBRID_1 = Config(0, 1, 0, 1, 0, 0)
HYBRID_2 = Config(0, 0, 1, 1, 0, 0.2)
HYBRID_3 = Config(0.75, 0.25, 0, 0.5, 0.5, 5)

DS_STORE = '.DS_Store'

def output_path():
    try:
        files = os.listdir('out')
    except FileNotFoundError:
        os.mkdir('out')
        files = os.listdir('out')
    if DS_STORE in files:
        os.remove(f'./out/{DS_STORE}')
        files.remove(DS_STORE)
    indices = map(lambda f: int(f.split('.')[0][-1]), files)
    i = max(indices, default=-1) + 1

    return f'./out/out{i}.wav'

######################
###   DEPRECATED   ###
######################

def next_power_of_2(x):
    return 1 if not x else 2 ** (x - 1).bit_length()

def get_amplitude(point):
    real, imag = point.real, point.imag
    amplitude = np.sqrt((real ** 2) + (imag ** 2))
    # return np.abs(point)
    return amplitude

def get_phase(point):
    real, imag = point.real, point.imag
    # phase = np.arctan2(imag, real)
    # if real > 0:
    #     phase = np.arctan(imag / real)
    # else:
    #     phase = np.arctan(imag / real) + np.pi
    # phase = np.angle(point)
    return phase

get_amplitude_vectorized = np.vectorize(get_amplitude, otypes=[float])
get_phase_vectorized = np.vectorize(get_phase, otypes=[float])
