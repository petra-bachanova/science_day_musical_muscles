## Neuro SpikerBox real-time EMG to audio converter

### Overview
This repository contains Python scripts for reading and processing data from a SpikerBox, a device used for recording Electromyography (EMG) data. Processing includes converting signals to audible sounds.

### Contents

- `spikerbox_realtime_analysis_and_audio.py`: Read & analyse data from the SpikerBox via serial communication in real time.
- `spikerbox_offline_analysis_and_audio.py`: Read & analyse .wav data recorded from the SpikerBox. Could be used to analyse & play other .wav data 

### Usage for Real time analysis

1. **Connect the SpikerBox**: Connect via USB, make sure it is visible in COM/serial ports. For Mac: `ls /dev/tty.usb*`

2. **Run the script**: Execute `spikerbox_realtime_analysis_and_audio`. There are two modes: `record_participant_baseline = True` outputs participant's frequency range, if set to False, it plays the processed EMG signal.

### Dependencies
Tested using Python 3.9.\
Install dependencies from requirements.txt

---
This project is built upon the core code from [SpikerStream Python repository](https://github.com/PHYS3888/SpikerStream/tree/master/SpikerStream_Python)