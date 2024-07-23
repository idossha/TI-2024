#!/usr/bin/env python3

'''
TI waveform illustration for publication 

Ido Haber
July 2024

'''

import numpy as np
import matplotlib.pyplot as plt
import argparse

def generate_waveform(f1, f2, A1, A2, t_start, t_end, sampling_rate):
    t = np.linspace(t_start, t_end, int(sampling_rate * (t_end - t_start)))
    signal1 = A1 * np.sin(2 * np.pi * f1 * (t + 0.5))
    signal2 = A2 * np.sin(2 * np.pi * f2 * t)
    interference = signal1 + signal2
    
    return t, signal1, signal2, interference

def plot_waveform(t, interference1, interference2, combined_interference, f1, f2, f3, f4, A1, A2, filename_base):
    plt.figure(figsize=(10, 10))
    
    plt.subplot(4, 1, 1)
    plt.plot(t, interference1, label=f'TI Signal 1: {f1} Hz and {f2} Hz', color='blue')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(4, 1, 2)
    plt.plot(t, interference2, label=f'TI Signal 2: {f3} Hz and {f4} Hz', color='orange')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(4, 1, 3)
    plt.plot(t, combined_interference, label='Combined TI Signal', color='green')
    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{filename_base}.png')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Generate and plot TI waveforms.')
    parser.add_argument('-f1', type=float, required=True, help='Frequency of first signal in Hz')
    parser.add_argument('-f2', type=float, required=True, help='Frequency of second signal in Hz')
    parser.add_argument('-f3', type=float, required=True, help='Frequency of third signal in Hz')
    parser.add_argument('-f4', type=float, required=True, help='Frequency of fourth signal in Hz')
    parser.add_argument('-t_end', type=float, default=2, help='End time in seconds (default: 2)')
    parser.add_argument('-sr', type=float, help='Sampling rate in Hz (default: 10 * max(f1, f3))')

    args = parser.parse_args()
    
    f1 = args.f1
    f2 = args.f2
    f3 = args.f3
    f4 = args.f4
    t_end = args.t_end
    sampling_rate = args.sr if args.sr else 10 * max(f1, f3)
    A1 = 1
    A2 = 1
    t_start = 0

    t1, _, _, interference1 = generate_waveform(f1, f2, A1, A2, t_start, t_end, sampling_rate)
    t2, _, _, interference2 = generate_waveform(f3, f4, A1, A2, t_start, t_end, sampling_rate)
    
    combined_interference = interference1 + interference2
    t = t1  # t1 and t2 are the same since they are generated with the same parameters

    plot_waveform(t, interference1, interference2, combined_interference, f1, f2, f3, f4, A1, A2, 'combined_interference_waveform')

if __name__ == '__main__':
    main()
