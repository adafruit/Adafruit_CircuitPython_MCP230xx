# SPDX-FileCopyrightText: 2021 Red_M
#
# SPDX-License-Identifier: MIT

"""
`mcp230xx`
====================================================

CircuitPython module for the MCP23017, MCP23008 I2C and MCP23S17, MCP23S08 SPI I/O extenders.

* Author(s): Red_M
"""

from adafruit_bus_device import i2c_device, spi_device

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# pylint: disable=too-few-public-methods
class MCP23XXX:
    """Base class for MCP23xxx devices."""

    def __init__(self, bus_device, address, chip_select=None, baudrate=100000):
        if chip_select is None:
            self._device = i2c_device.I2CDevice(bus_device, address)
        else:
            self._device = spi_device.SPIDevice(
                bus_device, chip_select, baudrate=baudrate
            )
