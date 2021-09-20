# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
# SPDX-FileCopyrightText: 2021 Pat Satyshur
#
# SPDX-License-Identifier: MIT

# pylint: disable=too-many-public-methods

"""
`pca9554`
====================================================

CircuitPython module for PCA9554 compatible I2C I/O extenders.
There are quite a few variants that will work with this. A few
that I have found include: PCA9554, PCA9554A, PCAL9554

* Author(s): Tony DiCola, Pat Satyshur (2021)
"""

from micropython import const
from .mcp230xx import MCP230XX
from .digital_inout import DigitalInOut

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

_PCA9554_ADDRESS = const(0x27)

_PCA9554_INPUT = const(0x00)	#Input register
_PCA9554_OUTPUT = const(0x01)	#Output register
_PCA9554_IPOL = const(0x02)		#Polarity inversion register
_PCA9554_IODIR = const(0x03)	#Configuration (direction) register

class PCA9554(MCP230XX):
    """Supports PCA9554 instance on specified I2C bus and optionally
    at the specified I2C address.
    """

    def __init__(self, i2c, address=_PCA9554_ADDRESS, reset=True):
        super().__init__(i2c, address)
        if reset:
            # Reset to all inputs, and no inverted polarity.
            self.iodir = 0xFF		#Set all IOs to inputs
            self.ipol = 0x00		#Set polatiry inversion off for all pins

    @property
    def gpio(self):
        """Returns the GPIO input register. This register contains the incoming
        logic level of the pins, regardless of whether they are set as an input
        or an output. Each bit represents the output value of the associated pin 
        (0 = low, 1 = high).
        
        Note: Based on the errata in the datasheet, the command byte must be changed
        to something other than 0x00 after reading from address 0x00 (the input register).
        Not doing this will cause the interrup pin to not operate correctly.
        """
        InputState = self._read_u8(_PCA9554_INPUT)
        self._read_u8(_PCA9554_OUTPUT) #Change command byte to 0x01
        return InputState

    @gpio.setter
    def gpio(self, val):
        """Set the value of the pins by writing to the output register. Bit values
        in this register have no effect on pins that are defined as inputs.        
        """
        self._write_u8(_PCA9554_OUTPUT, val)

    @property
    def iodir(self):
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output.
        """
        return self._read_u8(_PCA9554_IODIR)

    @iodir.setter
    def iodir(self, val):
        self._write_u8(_PCA9554_IODIR, val)

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this PCA9554 device.
        """
        if not 0 <= pin <= 7:
            raise ValueError("Pin number must be 0-7.")
        return DigitalInOut(pin, self)

    @property
    def ipol(self):
        """The raw IPOL output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self._read_u8(_PCA9554_IPOL)

    @ipol.setter
    def ipol(self, val):
        self._write_u8(_PCA9554_IPOL, val)