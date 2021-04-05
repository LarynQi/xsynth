import soundfile as sf
import numpy as np
import sys
import os

from utils import cart_to_pol, pol_to_cart
from utils import SOUND_1, SOUND_2, HYBRID_1, HYBRID_2, Config

DS_STORE = '.DS_Store'

def next_power_of_2(x):
    return 1 if not x else 2 ** (x - 1).bit_length()

def main(sound1, sound2, config=HYBRID_2):
    print('xsynth.py - cross synthesis')
    x, srx = sf.read(sound1)
    h, srh = sf.read(sound2)
    print(h)
    if srx != srh:
        sys.exit('Inconsistent sampling rate')

    # n = next_power_of_2(max(x.shape[0], h.shape[0]))
    
    x_len, h_len = x.shape[0], h.shape[0]
    if x_len > h_len:
        loops = (x_len - h_len) // h_len
        h = np.tile(h, loops)
        diff = x_len - h.shape[0]
        # h = np.pad(h, diff, mode='constant')
    n = max(x.shape[0], h.shape[0])

    # sys.exit()

    # x_cart, h_cart = np.fft.rfft(x, n=n), np.fft.rfft(h, n=n)
    x_cart, h_cart = np.fft.rfft(x, n=n), np.fft.rfft(h, n=n)

    print(h_cart)
    x_amp, x_phase = cart_to_pol(x_cart)
    h_amp, h_phase = cart_to_pol(h_cart)

    # X, x, Q, Y, y = 1, 0, 0, 1, 0
    # X, x, Q, Y, y = 0, 1, 0, 0, 1
    # X, x, Q, Y, y = 0, 1, 0, 1, 0
    # X, x, Q, Y, y = 0, 0, 1, 1, 0

    # noise = 0.2

    X, x, Q, Y, y, noise = config.get_configurations()

    print(X, x, Q, Y, y)
    # sys.exit()
    print(h_amp)
    h_amp = np.vectorize(lambda val: val if val > noise else 0., otypes=[float])(h_amp)
    x_amp = np.vectorize(lambda val: val if val > noise else 0., otypes=[float])(x_amp)
    print(h_amp)
    # out_amp = (X * x_amp) + (x * h_amp) + (Q * np.sqrt(np.square(x_amp) + np.square(h_amp)))
    out_amp = (X * x_amp) + (x * h_amp) + (Q * np.sqrt(x_amp * h_amp))
    out_phase = (Y * x_phase) + (y * h_phase)

    print((out_amp == h_amp).all())
    print((out_phase == h_phase).all())

    out_cart = pol_to_cart(out_amp, out_phase)
    print(out_cart)
    out = np.fft.irfft(out_cart)
    out *= 0.5
    # print((out_cart == x_cart).all())
    # print(np.fft.irfft(x_cart, n=n))
    print(out, h)
    print(out.shape, h.shape)
    # sys.exit()
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
    sf.write(f'./out/out{i}.wav', out, srx)

if __name__ == '__main__':
    # main('Beethoven_Symph7.wav', 'radiohead.wav', config=SOUND_2)

    main('samples/Beethoven_Symph7.wav', 'samples/radiohead.wav', config=Config(1, 0, 1, 0, 1, 5))
