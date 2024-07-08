'''
TI waveform illustration for publication 

Ido Haber
July 2024

'''

import numpy as np
import matplotlib.pyplot as plt

def generate_waveform(f1, f2, A1, A2, t_start, t_end, sampling_rate):
    t = np.linspace(t_start, t_end, int(sampling_rate * (t_end - t_start)))
    signal1 = A1 * np.sin(2 * np.pi * f1 * t)
    signal2 = A2 * np.sin(2 * np.pi * f2 * t)
    interference = signal1 + signal2
    
    return t, signal1, signal2, interference

def plot_waveform(t, signal1, signal2, interference, f1, f2, A1, A2, filename_base):
    plt.figure(figsize=(10, 6))
    
    plt.subplot(3, 1, 1)
    plt.plot(t, signal1, label=f'Signal 1: {f1} Hz, {A1} Amplitude')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(t, signal2, label=f'Signal 2: {f2} Hz, {A2} Amplitude', color='orange')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(t, interference, label='Interference Signal', color='blue')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{filename_base}.png')
    plt.show()

# Example usage
f1 = 100  # Frequency of first signal in Hz
f2 = 106  # Frequency of second signal in Hz
A1 = 1  # Amplitude of first signal
A2 = 1  # Amplitude of second signal
t_start = 0  # Start time in seconds
t_end = 2  # End time in seconds
sampling_rate = 1000  # Sampling rate in Hz

t, signal1, signal2, interference = generate_waveform(f1, f2, A1, A2, t_start, t_end, sampling_rate)
plot_waveform(t, signal1, signal2, interference, f1, f2, A1, A2, 'interference_waveform')
