import serial
import numpy as np
# import plotly as plt
import matplotlib.pyplot as plt

# Define the COM port and baud rate
COM_PORT = 'COM10'
BAUD_RATE = 230400  # Adjust to match the baud rate of your SpikerBox

# Create a serial objects
ser = serial.Serial(COM_PORT, BAUD_RATE)
inputBufferSize = 10000 # 20000 = 1 second
ser.timeout = inputBufferSize/20000.0  # set read timeout

def read_arduino(ser,inputBufferSize):

    data = ser.read(inputBufferSize)
    out = [(int(data[i])) for i in range(0,len(data))]

    return out


def process_data(data):

    data_in = np.array(data)
    result = []
    i = 1

    while i < len(data_in)-1:
        if data_in[i] > 127:
            # Found beginning of frame
            # Extract one sample from 2 bytes
            intout = (np.bitwise_and(data_in[i],127))*128
            i = i + 1
            intout = intout + data_in[i]
            result = np.append(result,intout)
        i=i+1

    return result

# Check if the port was opened successfully
if ser.is_open:
    print(f"Serial port {COM_PORT} opened successfully.")
else:
    print(f"Failed to open serial port {COM_PORT}.")
    exit()  # Exit the script if the port was not opened successfully

try:
    # Read data from the serial port
    while True:

        total_time = 20.0; # time in seconds [[1 s = 20000 buffer size]]
        max_time = 10.0; # time plotted in window [s]
        N_loops = 20000.0/inputBufferSize*total_time

        T_acquire = inputBufferSize/20000.0    # length of time that data is acquired for
        N_max_loops = max_time/T_acquire    # total number of loops to cover desire time window

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.ion()
        fig.show()
        fig.canvas.draw()

        k = 0
        #while True:
        while k < N_loops: #Will end early so can't run forever.
            data = read_arduino(ser,inputBufferSize)
            data_temp = process_data(data)

            if k <= N_max_loops:

                if k==0:
                    data_plot = data_temp
                else:
                    data_plot = np.append(data_temp,data_plot)

                t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot))

            else:

                data_plot = np.roll(data_plot,len(data_temp))
                data_plot[0:len(data_temp)] = data_temp

            t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot))


        #    plt.xlim([0,max_time])
            ax1.clear()
            ax1.set_xlim(0, max_time)
            plt.xlabel('time [s]')
            ax1.plot(t,data_plot)
            fig.canvas.draw()
            plt.draw()
            plt.pause(0.001)
            print(data_plot,t)
            k += 1


except KeyboardInterrupt:
    # Close the serial port when the program is interrupted
    ser.close()
    print("Serial port closed.")
