# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
#
# SPDX-License-Identifier: MIT

"""
`mcp23008`
====================================================

CircuitPython module for the MCP23008 I2C I/O extenders.

* Author(s): Tony DiCola

Implementation Notes
--------------------

**Hardware:**

* `MCP23008 - i2c 8 input/output port expander
  <https://www.adafruit.com/product/593>`_

"""

from micropython import const

from .digital_inout import DigitalInOut
from .mcp230xx import MCP230XX

try:
    from typing import List

    from busio import I2C
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

_MCP23008_ADDRESS = const(0x20)
_MCP23008_IODIR = const(0x00)
_MCP23008_IPOL = const(0x01)
_MCP23008_GPINTEN = const(0x02)
_MCP23008_DEFVAL = const(0x03)
_MCP23008_INTCON = const(0x04)
_MCP23008_IOCON = const(0x05)
_MCP23008_GPPU = const(0x06)
_MCP23008_INTF = const(0x07)
_MCP23008_INTCAP = const(0x08)
_MCP23008_GPIO = const(0x09)


class MCP23008(MCP230XX):
    """Supports MCP23008 instance on specified I2C bus and optionally
    at the specified I2C address.
    """

    def __init__(self, i2c: I2C, address: int = _MCP23008_ADDRESS, reset: bool = True) -> None:
        super().__init__(i2c, address)

        if reset:
            # Reset to all inputs with no pull-ups and no inverted polarity.
            self.iodir = 0xFF
            self.gppu = 0x00
            self._write_u8(_MCP23008_IPOL, 0x00)

    @property
    def gpio(self) -> int:
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23008_GPIO)

    @gpio.setter
    def gpio(self, val: int) -> None:
        self._write_u8(_MCP23008_GPIO, val)

    @property
    def iodir(self) -> int:
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23008_IODIR)

    @iodir.setter
    def iodir(self, val: int) -> None:
        self._write_u8(_MCP23008_IODIR, val)

    @property
    def gppu(self) -> int:
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23008_GPPU)

    @gppu.setter
    def gppu(self, val: int) -> None:
        self._write_u8(_MCP23008_GPPU, val)

    def get_pin(self, pin: int) -> DigitalInOut:
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23008 device.
        """
        if not 0 <= pin <= 7:
            raise ValueError("Pin number must be 0-7.")
        return DigitalInOut(pin, self)

    @property
    def ipol(self) -> int:
        """The raw IPOL output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self._read_u8(_MCP23008_IPOL)

    @ipol.setter
    def ipol(self, val: int) -> None:
        self._write_u8(_MCP23008_IPOL, val)

    @property
    def interrupt_configuration(self) -> int:
        """The raw INTCON interrupt control register. The INTCON register
        controls how the associated pin value is compared for the
        interrupt-on-change feature. If  a  bit  is  set,  the  corresponding
        I/O  pin  is  compared against the associated bit in the DEFVAL
        register. If a bit value is clear, the corresponding I/O pin is
        compared against the previous value.
        """
        return self._read_u8(_MCP23008_INTCON)

    @interrupt_configuration.setter
    def interrupt_configuration(self, val: int) -> None:
        self._write_u8(_MCP23008_INTCON, val)

    @property
    def interrupt_enable(self) -> int:
        """The raw GPINTEN interrupt control register. The GPINTEN register
        controls the interrupt-on-change feature for each pin. If a bit is
        set, the corresponding pin is enabled for interrupt-on-change.
        The DEFVAL and INTCON registers must also be configured if any pins
        are enabled for interrupt-on-change.
        """
        return self._read_u8(_MCP23008_GPINTEN)

    @interrupt_enable.setter
    def interrupt_enable(self, val: int) -> None:
        self._write_u8(_MCP23008_GPINTEN, val)

    @property
    def default_value(self) -> int:
        """The raw DEFVAL interrupt control register. The default comparison
        value is configured in the DEFVAL register. If enabled (via GPINTEN
        and INTCON) to compare against the DEFVAL register, an opposite value
        on the associated pin will cause an interrupt to occur.
        """
        return self._read_u8(_MCP23008_DEFVAL)

    @default_value.setter
    def default_value(self, val: int) -> None:
        self._write_u8(_MCP23008_DEFVAL, val)

    @property
    def io_control(self) -> int:
        """The raw IOCON configuration register. Bit 1 controls interrupt
        polarity (1 = active-high, 0 = active-low). Bit 2 is whether irq pin
        is open drain (1 = open drain, 0 = push-pull). Bit 3 is unused.
        Bit 4 is whether SDA slew rate is enabled (1 = yes). Bit 5 is if I2C
        address pointer auto-increments (1 = no). Bit 6 is unused. Bit 7 is
        unused.
        """
        return self._read_u8(_MCP23008_IOCON)

    @io_control.setter
    def io_control(self, val: int) -> None:
        val &= ~0x80
        self._write_u8(_MCP23008_IOCON, val)

    @property
    def int_flag(self) -> List[int]:
        """Returns a list with the pin numbers that caused an interrupt
        pins 0-7
        """
        intf = self._read_u8(_MCP23008_INTF)
        flags = [pin for pin in range(8) if intf & (1 << pin)]
        return flags

     @property
    def int_cap(self) -> List[int]:
        """Returns a list with the pin values at time of interrupt
        pins 0-7
        """
        intcap = self._read_u8(_MCP23008_INTCAP)
        return [(intcap >> pin) & 1 for pin in range(8)]

    def clear_ints(self) -> None:
        """Clears interrupts by reading INTCAP."""
        self._read_u8(_MCP23008_INTCAP)
