# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
#
# SPDX-License-Identifier: MIT

"""
`mcp23Sxx`
====================================================

CircuitPython module for the MCP23S17 SPI I/O extenders.

* Author(s): Tony DiCola
* Contributors(s): Romy Bompart (2020)
"""

from adafruit_bus_device.spi_device import SPIDevice

__version__ = ""
__repo__ = ""

# shared between both the MCP23S17 class to reduce memory allocations.
# However this is explicitly not thread safe or re-entrant by design!
# Header to start a reading or writting operation
MCP23SXX_CODE_READ  = 0x41
MCP23SXX_CODE_WRITE = 0x40

# pylint: disable=too-few-public-methods
class MCP23SXX:
    """Base class for MCP23Sxx devices."""

    def __init__(self, spi_bus, cs, address):
        self._spi_device = SPIDevice(spi_bus, cs)
        self._out_buf   = bytearray(4)
        self._in_buf    = bytearray(4)
        self.cmd_write  = MCP23SXX_CODE_WRITE | (address << 1)
        self.cmd_read   = MCP23SXX_CODE_READ | (address << 1)

    def _read_u16le(self, register):
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        self._out_buf [0] = self.cmd_read
        self._out_buf [1] = register & 0xFF
        with self._spi_device as spi:
            spi.write_readinto(self._out_buf, self._in_buf)
        return (self._in_buf[3] << 8) | self._in_buf[2]

    def _write_u16le(self, register, value):
        # Write an unsigned 16 bit little endian value to the specified 8-bit
        # register.
        self._out_buf [0] = self.cmd_write
        self._out_buf [1] = register & 0xFF
        self._out_buf [2] = (value & 0xFF)
        self._out_buf [3] = (value >> 8) & 0xFF
        with self._spi_device as spi:
            spi.write(self._out_buf)


    def _read_u8(self, register):
        # Read an unsigned 8 bit value from the specified 8-bit register.
        self._out_buf [0] = self.cmd_read
        self._out_buf [1] = register & 0xFF
        with self._spi_device as spi:
            spi.write_readinto(self._out_buf, self._in_buf)
        return self._in_buf[2]

    def _write_u8(self, register, value):
        # Write an 8 bit value to the specified 8-bit register.
        self._out_buf [0] = self.cmd_write
        self._out_buf [1] = register & 0xFF
        self._out_buf [2] = value & 0xFF
        with self._spi_device as spi:
            spi.write(self._out_buf, end = 3)