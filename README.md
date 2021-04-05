# xsynth

### Quickstart

1. Create a virtualenv

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
_Note: Developed and tested on Python 3.7.4_

2. Run

```sh
python3 xsynth.py
```

Outputs can be found in `xsynth/out`

3. [Optional] Use custom samples
- Move audio samples (e.g. .wav files) to `xsynth/samples`
- Change the `sound1` and `sound2` arguments to `main`
- [Optional] Use your own configuration by creating a `Config` instance and passing it into `main`

### Algorithm
1. Read in two sound files, `s1` and `s2`, as numpy arrays
2. Pad numpy arrays to handle mismatching dimensions (samples of unequal length)
    - Shorter sample is looped to match the length of the longer sample
3. Run FFT on `s1` and `s2`, returning their spectrum with amplitude and frequency information in the frequency domain. The data is in cartesian (complex) coordinates, `s1_cart` and `s2_cart`
4. Convert to polar to extract the amplitude and phase individually, returning `s1_amp`, `s1_phase`, `s2_amp`, `s2_phase`.
5. Filter noise based on threshold, `noise_threshold`
6. Apply cross-synthesis combination to produce the output spectrum, `out_amp` and `out_phase` using the weights `X`, `x`, `Q`, `Y`, `y`:

<img src="https://render.githubusercontent.com/render/math?math=out_{amp} = X s1_{amp} %2B x s2_{amp} %2B Q(\sqrt{s1_{amp} s2_{amp}})">

<img src="https://render.githubusercontent.com/render/math?math=out_{phase} = Y s1_{phase} %2B y s2_{phase}">

7. Convert output spectrum from polar to cartesian (complex) coordinates, `out_cart`.

8. Transform the output specturm from the frequency domain to a signal in the time domain using inverse FFT.

9. Write the resulting numpy array into a .wav file. We are done!

### Design

- All the high-level algorithm steps are executed in `xsynth.py`
- The nitty-gritty of the specific steps such as coordinate conversion and noise filtration is handled in `utils.py`
    - Originally wrote a lot of the mathematical conversion functions myself and vectorized them to apply to numpy arrays, but deprecated them in favor of using the built-in `np.abs` and `np.angle` (for amplitude and phase respectively)
- The configuration system is also handled in `utils.py`. Users can create new configurations for the cross-synthesis by creating new `Config` objects and passing them into `main`.
    - `utils.py` also exports a few default configurations: `SOUND_1`, `SOUND_2`, `HYBRID_1`, `HYBRID_2`, `HYBRID_3`.
- Lastly, auxiliary tasks such as file writing is done `utils.py`

### Example Outputs

- See the `xsynth/examples` directory (link)
