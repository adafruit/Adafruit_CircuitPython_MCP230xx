# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
# SPDX-FileCopyrightText: 2021 Red_M
#
# SPDX-License-Identifier: MIT

"""
`MCP23S08`
====================================================

CircuitPython module for the MCP23S08 I2C I/O extenders.

* Author(s): Tony DiCola, Romy Bompart (2020), Red_M (2021)
"""

from micropython import const
from .mcp23sxx import MCP23SXX
from .digital_inout import DigitalInOut

try:
    import typing  # pylint: disable=unused-import
    from busio import SPI
    import digitalio
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP23Sxx.git"

_MCP23S08_ADDRESS = const(0x20)
_MCP23S08_IODIR = const(0x00)
_MCP23S08_IPOL = const(0x01)
_MCP23S08_GPINTEN = const(0x02)
_MCP23S08_DEFVAL = const(0x03)
_MCP23S08_INTCON = const(0x04)
_MCP23S08_IOCON = const(0x05)
_MCP23S08_GPPU = const(0x06)
_MCP23S08_INTF = const(0x07)
_MCP23S08_INTCAP = const(0x08)
_MCP23S08_GPIO = const(0x09)


# pylint: disable=too-many-arguments
class MCP23S08(MCP23SXX):
    """Supports MCP23S08 instance on specified I2C bus and optionally
    at the specified I2C address.
    """

    def __init__(
        self,
        spi: SPI,
        chip_select: digitalio.DigitalInOut,
        address: int = _MCP23S08_ADDRESS,
        reset: bool = True,
        baudrate: int = 100000,
    ) -> None:
        super().__init__(spi, address, chip_select, baudrate=baudrate)
        # For user information
        self.address = address
        if reset:
            # Reset to all inputs with no pull-ups and no inverted polarity.
            self.iodir = 0xFF
            self.gppu = 0x00
            self._write_u8(_MCP23S08_IPOL, 0x00)

    @property
    def gpio(self) -> int:
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23S08_GPIO)

    @gpio.setter
    def gpio(self, val: int) -> None:
        self._write_u8(_MCP23S08_GPIO, val)

    @property
    def iodir(self) -> int:
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23S08_IODIR)

    @iodir.setter
    def iodir(self, val: int) -> None:
        self._write_u8(_MCP23S08_IODIR, val)

    @property
    def gppu(self) -> int:
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23S08_GPPU)

    @gppu.setter
    def gppu(self, val: int) -> None:
        self._write_u8(_MCP23S08_GPPU, val)

    def get_pin(self, pin: int) -> DigitalInOut:
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23S08 device.
        """
        if not 0 <= pin <= 7:
            raise ValueError("Pin number must be 0-7.")
        return DigitalInOut(pin, self)
