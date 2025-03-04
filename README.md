# TLPM-Linux
This is a python package for interfacing with ThorLabs power meters from a Linux platform.

The tlpmSCPI package is intended to allow communication with a ThorLabs PM16-130 compact usb power meter. ThorLabs provides software to interact with the device, but the provided software only supports Windows. This software is designed to extend support to unix based systems. Furthermore, support can be extended to ARM architecture using the pure python backend in the PyVISA library. The tlpmSCPI package will still work on Windows computers, but the os isn't fully supported because most of the capabilities are already provided by the ThorLabs software.

# Environment Variable
Each power meter will have a unique serial number which will determine the usb address. In order to use the package, the environment variable 'SERIAL_TL_PM16_130' will need to be set to this serial number so that the tlpmSCPI package can find the device.

# UDev Rules
On Linux systems that utilize udev rules to manage permissions to peripheral devices, the following line should be added to a udev rules file such as /etc/udev/rules.d/10-local.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="1313", ATTR{idProduct}=="807b", MODE="0666"

# Scripts
profiler_repl.py in the scripts folder is a simple script that depends only on numpy, scipy, and matplotlib which allows for the rapid collection of data for profiling a laser beam. An inexpensive way of measuring a laser profile is to block the beam with something like a razer blade edge and measure the total power transmitted. If the power transmitted is recorded as a function of blade edge position, the marginal profile of the laser beam can be estimated. The issue with this process is that it takes a long time to measure a beam profile if the positions and powers from the data must be recorded manually. profiler_repl.py is a short REPL program that is designed to quickly fetch power measurements using the tlpmSCPI package and user input in order to quickly record measurements. Furthermore, if the razor edge is moved in regular intervals, the REPL can be set to assume the same spacing between all measurements. In this case, a profile measurement can recorded without any manual typing or writing of any numbers. One entry is needed for the first input, and all successive measurements can be recorded using only the enter key.

