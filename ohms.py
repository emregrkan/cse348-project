import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, fftshift, ifft
import sounddevice as sd
import soundfile as sf

def bpflt(f, freq):
    hf = 40e3
    return np.where(
        np.logical_or(np.logical_and(freq >= f - hf, freq <= f + hf),
        np.logical_and(freq >= -f - hf, freq <= -f + hf)),
        1.0, 0.0
    )

def lpflt(f, freq):
    return np.where(np.logical_and(freq >= -f, freq <= f), 1.0, 0.0)

def main():
    fs = 96000
    seconds = 3
    rec_in_tmod = np.loadtxt('93.txt')
    time = np.linspace(0, seconds, rec_in_tmod.shape[0])
    freq = np.linspace(-fs/2, fs/2, fs*seconds)
    rec_in_fmod = fftshift(fft(rec_in_tmod))

    f1, f2 = 5000, 12000
    bp1, lp1 = bpflt(f1, freq), lpflt(f1, freq)
    bp2, lp2 = bpflt(f2, freq), lpflt(f2, freq)
    
    bpfiltered1 = np.multiply(rec_in_fmod, bp1)
    bpfiltered1_mult = fftshift(fft(np.multiply(ifft(fftshift(bpfiltered1)), np.cos(2*np.pi*f1*time))))
    lpfiltered1 = np.multiply(bpfiltered1_mult, lp1)

    bpfiltered2 = np.multiply(rec_in_fmod, bp2)
    bpfiltered2_mult = fftshift(fft(np.multiply(ifft(fftshift(bpfiltered2)), np.cos(2*np.pi*f2*time))))
    lpfiltered2 = np.multiply(bpfiltered2_mult, lp2)

    res1, res2 = ifft(fftshift(lpfiltered1)), ifft(fftshift(lpfiltered2))

    sd.play(np.real(res1), fs, blocking=True) # vast majority - fox majority
    sd.play(np.real(res2), fs, blocking=True) # famous blue?

    sf.write('messag1.wav', np.real(res1), fs)
    sf.write('message2.wav', np.real(res2), fs)


if __name__ == '__main__':
    main()