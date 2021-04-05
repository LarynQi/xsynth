import soundfile as sf
import numpy as np
import sys

from utils import Config, SOUND_1, SOUND_2, HYBRID_1, HYBRID_2, HYBRID_3
from utils import cart_to_pol, pol_to_cart
from utils import filter_noise
from utils import output_path

def main(sound1, sound2, config=HYBRID_3):
    print('MUSIC159: cross-synthesis')
    print('executing...')
    s1, sr_1 = sf.read(sound1)
    s2, sr_2 = sf.read(sound2)

    if sr_1 != sr_2:
        sys.exit('Inconsistent sampling rate')
    
    s1_len, s2_len = s1.shape[0], s2.shape[0]
    
    if s1_len > s2_len:
        loops = (s1_len - s2_len) // s2_len
        s2 = np.tile(s2, loops)
        # remainder = s1_len - s2.shape[0]
        # s2 = np.append(s2, s2[:remainder])
        # s2 = np.pad(s2, diff, mode='constant')
    else:
        loops = (s2_len - s1_len) // s1_len
        s1 = np.tile(s1, loops)
        # remainder = s2_len - s1.shape[0]
        # s1 = np.append(s1, s1[:remainder])
    
    n = max(s1.shape[0], s2.shape[0])
    s1_cart, s2_cart = np.fft.rfft(s1, n=n), np.fft.rfft(s2, n=n)

    s1_amp, s1_phase = cart_to_pol(s1_cart)
    s2_amp, s2_phase = cart_to_pol(s2_cart)

    X, x, Q, Y, y, noise_threshold = config.get_configurations()

    s1_amp = filter_noise(s1_amp, noise_threshold)
    s2_amp = filter_noise(s2_amp, noise_threshold)

    out_amp = (X * s1_amp) + (x * s2_amp) + (Q * np.sqrt(s1_amp * s2_amp))
    out_phase = (Y * s1_phase) + (y * s2_phase)

    out_cart = pol_to_cart(out_amp, out_phase)

    out = np.fft.irfft(out_cart, n=n)

    sf.write(output_path(), out, sr_1)
    print('done!')

if __name__ == '__main__':
    main('samples/Beethoven_Symph7.wav', 'samples/radiohead.wav')
