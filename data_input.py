"""
for fresh installation on Mac:

pip install pyusb
brew install libusb
"""

import usb.core
import usb.util

# Vendor ID and Product ID of the USB devices
VENDOR_ID = 0x0403
PRODUCT_ID = 0x6015

# Find the USB device
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if device is None:
    raise ValueError("Device not found")

try:
    # Detach kernel driver if it's attached
    if device.is_kernel_driver_active(0):
        device.detach_kernel_driver(0)

    # Set configuration
    device.set_configuration()

    # Endpoint configuration
    endpoint = device[0][(0, 0)][0]

    # Read data from the endpoint
    data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)

    print("Data received:", data)

finally:
    # Release the device
    usb.util.dispose_resources(device)
