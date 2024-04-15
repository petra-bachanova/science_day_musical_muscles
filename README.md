# "Make your muscles sing" Neuro SpikerBox Science Day Project

### Dependencies

* pyusb
* libusb

### Installing

On Petra's Mac - some difficulties with installing `pyusb` and `libusb`. This seems to be related to the M1 chip on the laptop. It seems that some link between `libusb` and `pyusb` only works when python has been installed via `homebrew`. Steps I took to solve this:

```commandline
brew install libusb
brew install python@3.9
pip3.9 install pyusb
```

If this does not work, I also previously followed steps in this Stack Overflow thread (but I am not sure if these are necessary).

https://stackoverflow.com/questions/70729330/python-on-m1-mbp-trying-to-connect-to-usb-devices-nobackenderror-no-backend-a

### Executing program

`/opt/homebrew/bin/python3.9 /Users/Petra/Documents/repos/science_day/data_input.py`

`ls /dev/cu.*`
