# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
# SPDX-FileCopyrightText: 2021 Red_M
#
# SPDX-License-Identifier: MIT

"""
`mcp23sxx`
====================================================

CircuitPython module for the MCP23S17 SPI I/O extenders.

* Author(s): Romy Bompart (2020), Red_M (2021)
"""

from .mcp23xxx import MCP23XXX

try:
    import typing  # pylint: disable=unused-import
    from busio import SPI
    import digitalio
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# shared between both the MCP23S17 class to reduce memory allocations.
# However this is explicitly not thread safe or re-entrant by design!
# Header to start a reading or writting operation
_OUT_BUFFER = bytearray(4)
_IN_BUFFER = bytearray(4)
MCP23SXX_CODE_READ = 0x41
MCP23SXX_CODE_WRITE = 0x40

# pylint: disable=too-few-public-methods
class MCP23SXX(MCP23XXX):
    """Base class for MCP23Sxx devices."""

    def __init__(
        self,
        spi: SPI,
        address: int,
        chip_select: digitalio.DigitalInOut,
        baudrate: int = 100000,
    ) -> None:
        self.cmd_write = MCP23SXX_CODE_WRITE | (address << 1)
        self.cmd_read = MCP23SXX_CODE_READ | (address << 1)
        super().__init__(spi, address, chip_select, baudrate=baudrate)

    def _read_u16le(self, register: int) -> int:
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        _OUT_BUFFER[0] = self.cmd_read
        _OUT_BUFFER[1] = register & 0xFF
        with self._device as bus_device:
            bus_device.write_readinto(_OUT_BUFFER, _IN_BUFFER)
        return (_IN_BUFFER[3] << 8) | _IN_BUFFER[2]

    def _write_u16le(self, register: int, value: int) -> None:
        # Write an unsigned 16 bit little endian value to the specified 8-bit
        # register.
        _OUT_BUFFER[0] = self.cmd_write
        _OUT_BUFFER[1] = register & 0xFF
        _OUT_BUFFER[2] = value & 0xFF
        _OUT_BUFFER[3] = (value >> 8) & 0xFF
        with self._device as bus_device:
            bus_device.write(_OUT_BUFFER)

    def _read_u8(self, register: int) -> int:
        # Read an unsigned 8 bit value from the specified 8-bit register.
        _OUT_BUFFER[0] = self.cmd_read
        _OUT_BUFFER[1] = register & 0xFF
        with self._device as bus_device:
            bus_device.write_readinto(_OUT_BUFFER, _IN_BUFFER)
        return _IN_BUFFER[2]

    def _write_u8(self, register: int, value: int) -> None:
        # Write an 8 bit value to the specified 8-bit register.
        _OUT_BUFFER[0] = self.cmd_write
        _OUT_BUFFER[1] = register & 0xFF
        _OUT_BUFFER[2] = value & 0xFF
        with self._device as bus_device:
            bus_device.write(_OUT_BUFFER, end=3)
