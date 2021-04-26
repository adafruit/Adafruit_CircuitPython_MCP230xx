# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
#
# SPDX-License-Identifier: MIT

"""
`mcp230xx`
====================================================

CircuitPython module for the MCP23017, MCP23008 I2C and MCP23S17, MCP23S08 SPI I/O extenders.

* Author(s): Tony DiCola, Romy Bompart (2020), Red_M (2021)
"""

from adafruit_bus_device import i2c_device, spi_device

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# Global buffer for reading and writing registers with the devices.  This is
# shared between both the MCP23008 and MCP23017 class to reduce memory allocations.
# However this is explicitly not thread safe or re-entrant by design!
_BUFFER = bytearray(3)
MCP23SXX_CODE_READ = 0x41
MCP23SXX_CODE_WRITE = 0x40


# pylint: disable=too-few-public-methods
class MCP23XXX:
    """Base class for MCP230xx devices."""

    def __init__(self, bus_device, address, chip_select=None):
        if chip_select is None:
            self._device = i2c_device.I2CDevice(bus_device, address)
        else:
            self._device = spi_device.SPIDevice(bus_device, chip_select)
