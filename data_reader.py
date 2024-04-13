"""
For much of the source code for reading and processing the data, see:

https://github.com/PHYS3888/SpikerStream/tree/master/SpikerStream_Python

I used code from: SpikerStream_Linux_Live.py; but there are also files that might be useful if issues arise.
"""


import math
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy import signal
import musicpy as mp
import time

# Define the COM port and baud rate
COM_PORT = '/dev/tty.usbserial-DM89ON8K'
BAUD_RATE = 230400  # Adjust to match the baud rate of your SpikerBox

# Create a serial object
ser = serial.Serial(COM_PORT, BAUD_RATE)
inputBufferSize = 20000  # 20000 = 1 second
ser.timeout = inputBufferSize/20000.0  # set read timeout


def read_spikerbox_data(ser_, inputBufferSize_):
    """
    Read data from the spikerbox
    """

    data_ = ser_.read(inputBufferSize_)
    out = [(int(data_[i])) for i in range(0, len(data_))]

    return out


def process_data(data_):

    data_in = np.array(data_)
    result = []
    i = 1

    while i < len(data_in)-1:
        # >127 indicates the beginning of a frame of data?
        if data_in[i] > 127:
            # Extracts one sample from 2 bytes, performs a bitwise AND operation.
            # This clears the most significant bit, leaving only the lower 7 bits of the byte.
            # * 128 to shift those 7 bits to occupy the upper 7 bits of the 16-bit integer 'intout'
            intout = (np.bitwise_and(data_in[i], 127))*128
            # move to the next byte of data
            i = i + 1
            # add the next byte to the lower 7 bits of 'intout', combining the two bytes to form a 16-bit sample
            intout = intout + data_in[i]
            # append the combined 16-bit sample to the 'result' array
            result = np.append(result,  intout)
        i = i + 1

    return result


def notch_filter(f0, input_signal):
    # Design a notch filter to remove 60Hz power line interference
    fs_filter = 10000  # Sampling frequency of the signal
    # f0 = 60.006  # Frequency to be removed from the signal (60Hz)
    Q = 30.0  # Quality factor of the notch filter
    b, a = signal.iirnotch(f0, Q, fs_filter)
    # Apply the notch filter to the EMG signal
    filtered_signal_ = signal.filtfilt(b, a, input_signal)
    return filtered_signal_


def notch_filters(notch_frequencies, input_signal):

    filtered_signal_ = input_signal

    for f0 in notch_frequencies:

        # Design a notch filter to remove 60Hz power line interference
        fs_filter = 10000  # Sampling frequency of the signal
        # f0 = 60.006  # Frequency to be removed from the signal (60Hz)
        Q = 30.0  # Quality factor of the notch filter
        b, a = signal.iirnotch(f0, Q, fs_filter)
        # Apply the notch filter to the EMG signal
        filtered_signal_ = signal.filtfilt(b, a, filtered_signal_)

    return filtered_signal_


def rescale_frequency(frequency, min_recorded, max_recorded):
    c1_frequency = 32.7
    c5_frequency = 523.2
    # Calculate the number of full tones between the starting and ending frequencies in both scales
    recorded_frequency_range = max_recorded - min_recorded  # 69 steps
    c1_c5_frequency_range = c5_frequency - c1_frequency  # 490.5 steps
    stretch_factor = c1_c5_frequency_range / recorded_frequency_range

    new_frequency = (frequency - min_recorded) * stretch_factor + c1_frequency

    return new_frequency


def frequency_to_note(freq):
    # Convert frequency to note
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    try:
        note_number = 7 * math.log2(freq / 32.7)
    except Exception as e:
        print(freq)
        raise Exception(e)

    note_number = round(note_number)

    note_ = notes[(note_number - 1) % len(notes)]
    octave = (note_number + 1) // len(notes) + 1

    return f"{note_}{octave}"


record_participant_range = False
participant_min_freq, participant_max_freq = (40, 100)

# Check if the port was opened successfully
if ser.is_open:
    print(f"Serial port {COM_PORT} opened successfully.")
else:
    print(f"Failed to open serial port {COM_PORT}.")
    exit()  # Exit the script if the port was not opened successfully

all_frequencies = []
try:
    # Read data from the serial port
    while True:

        total_time = 40.0  # time in seconds [[1 s = 20000 buffer size]]
        max_time = 1.0  # time plotted in window [s]
        N_loops = 20000.0/inputBufferSize*total_time

        T_acquire = inputBufferSize/20000.0    # length of time that data is acquired for
        N_max_loops = math.floor(max_time/T_acquire)    # total number of loops to cover desire time window

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        plt.ion()
        fig.show()
        fig.canvas.draw()

        k = 0
        while k < N_loops:  # Will end early so can't run forever.
            data = read_spikerbox_data(ser, inputBufferSize)
            data_temp = process_data(data)

            if k <= N_max_loops:
                if k == 0:
                    data_plot = data_temp
                else:
                    data_plot = np.append(data_temp, data_plot)

                t = (min(k+1, N_max_loops))*inputBufferSize/20000.0*np.linspace(0, 1, len(data_plot))

            else:
                data_plot = np.roll(data_plot, len(data_temp))
                data_plot[0:len(data_temp)] = data_temp

            t = (min(k+1, N_max_loops))*inputBufferSize/20000.0*np.linspace(0, 1, len(data_plot))

            # plt.xlim([0,max_time])
            ax1.clear()
            ax1.set_xlim(0, 10)
            plt.xlabel('time [s]')
            ax1.plot(t, data_plot)
            fig.canvas.draw()
            plt.draw()
            plt.pause(0.001)
            # print(data_plot, t)
            k += 1



            # # Notch filter
            # filtered_signal = notch_filter(f0=60.06, input_signal=data_plot)
            # filtered_signal = notch_filter(f0=299, input_signal=filtered_signal)
            # filtered_signal = notch_filter(f0=59.8, input_signal=filtered_signal)

            notch_filter_frequencies = [60.06, 299, 59.8]
            filtered_signal = notch_filters(notch_filter_frequencies, input_signal=data_plot)

            sample_rate = 10000
            f, t, Sxx = spectrogram(filtered_signal, fs=sample_rate, nperseg=len(filtered_signal))
            # find the index of the maximum amplitude frequency & get the dominant frequency
            dominant_freq_index = np.argmax(Sxx, axis=0)
            dominant_freq = f[dominant_freq_index][0]

            # print(np.mean(data_plot))

            if record_participant_range:
                if dominant_freq < 500:
                    all_frequencies.append(dominant_freq)
                rescaled_freq = ""
                note = ""

            else:
                if participant_min_freq < dominant_freq < participant_max_freq:

                    rescaled_freq = rescale_frequency(
                        dominant_freq,
                        min_recorded=participant_min_freq,
                        max_recorded=participant_max_freq
                    )

                    note = frequency_to_note(rescaled_freq)
                    mp.play(mp.N(note), instrument=35)

                else:
                    time.sleep(0.5)
                    rescaled_freq = ""
                    note = ""

            print(f"Dominant, rescaled, note: {dominant_freq, rescaled_freq, note}")


except KeyboardInterrupt:
    # Close the serial port when the program is interrupted
    ser.close()
    print("Serial port closed.")
    if all_frequencies:
        print(min(all_frequencies), max(all_frequencies))
    else:
        print("all_frequencies list is empty!")


