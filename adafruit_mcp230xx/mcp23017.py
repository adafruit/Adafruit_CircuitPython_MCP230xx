# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
#
# SPDX-License-Identifier: MIT

"""
`mcp23017`
====================================================

CircuitPython module for the MCP23017 I2C I/O extenders.

* Author(s): Tony DiCola

Implementation Notes
--------------------

**Hardware:**

* `MCP23017 - i2c 16 input/output port expander
  <https://www.adafruit.com/product/732>`_

* `Adafruit MCP23017 I2C GPIO Expander Breakout - STEMMA QT / Qwiic
  <https://www.adafruit.com/product/5346>`_

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

_MCP23017_ADDRESS = const(0x20)
_MCP23017_IODIRA = const(0x00)
_MCP23017_IODIRB = const(0x01)
_MCP23017_IPOLA = const(0x02)
_MCP23017_IPOLB = const(0x03)
_MCP23017_GPINTENA = const(0x04)
_MCP23017_DEFVALA = const(0x06)
_MCP23017_INTCONA = const(0x08)
_MCP23017_IOCON = const(0x0A)
_MCP23017_GPPUA = const(0x0C)
_MCP23017_GPPUB = const(0x0D)
_MCP23017_GPIOA = const(0x12)
_MCP23017_GPIOB = const(0x13)
_MCP23017_INTFA = const(0x0E)
_MCP23017_INTFB = const(0x0F)
_MCP23017_INTCAPA = const(0x10)
_MCP23017_INTCAPB = const(0x11)


class MCP23017(MCP230XX):
    """Supports MCP23017 instance on specified I2C bus and optionally
    at the specified I2C address.
    """

    def __init__(self, i2c: I2C, address: int = _MCP23017_ADDRESS, reset: bool = True) -> None:
        super().__init__(i2c, address)
        if reset:
            # Reset to all inputs with no pull-ups and no inverted polarity.
            self.iodir = 0xFFFF
            self.gppu = 0x0000
            self.iocon = 0x4  # turn on IRQ Pins as open drain
            self._write_u16le(_MCP23017_IPOLA, 0x0000)

    @property
    def gpio(self) -> int:
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u16le(_MCP23017_GPIOA)

    @gpio.setter
    def gpio(self, val: int) -> None:
        self._write_u16le(_MCP23017_GPIOA, val)

    @property
    def gpioa(self) -> int:
        """The raw GPIO A output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23017_GPIOA)

    @gpioa.setter
    def gpioa(self, val: int) -> None:
        self._write_u8(_MCP23017_GPIOA, val)

    @property
    def gpiob(self) -> int:
        """The raw GPIO B output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23017_GPIOB)

    @gpiob.setter
    def gpiob(self, val: int) -> None:
        self._write_u8(_MCP23017_GPIOB, val)

    @property
    def iodir(self) -> int:
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u16le(_MCP23017_IODIRA)

    @iodir.setter
    def iodir(self, val: int) -> None:
        self._write_u16le(_MCP23017_IODIRA, val)

    @property
    def iodira(self) -> int:
        """The raw IODIR A direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23017_IODIRA)

    @iodira.setter
    def iodira(self, val: int) -> None:
        self._write_u8(_MCP23017_IODIRA, val)

    @property
    def iodirb(self) -> int:
        """The raw IODIR B direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23017_IODIRB)

    @iodirb.setter
    def iodirb(self, val: int) -> None:
        self._write_u8(_MCP23017_IODIRB, val)

    @property
    def gppu(self) -> int:
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u16le(_MCP23017_GPPUA)

    @gppu.setter
    def gppu(self, val: int) -> None:
        self._write_u16le(_MCP23017_GPPUA, val)

    @property
    def gppua(self) -> int:
        """The raw GPPU A pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23017_GPPUA)

    @gppua.setter
    def gppua(self, val: int) -> None:
        self._write_u8(_MCP23017_GPPUA, val)

    @property
    def gppub(self) -> int:
        """The raw GPPU B pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23017_GPPUB)

    @gppub.setter
    def gppub(self, val: int) -> None:
        self._write_u8(_MCP23017_GPPUB, val)

    def get_pin(self, pin: int) -> DigitalInOut:
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23017 device.
        """
        if not 0 <= pin <= 15:
            raise ValueError("Pin number must be 0-15.")
        return DigitalInOut(pin, self)

    @property
    def ipol(self) -> int:
        """The raw IPOL output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self._read_u16le(_MCP23017_IPOLA)

    @ipol.setter
    def ipol(self, val: int) -> None:
        self._write_u16le(_MCP23017_IPOLA, val)

    @property
    def ipola(self) -> int:
        """The raw IPOL A output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self._read_u8(_MCP23017_IPOLA)

    @ipola.setter
    def ipola(self, val: int) -> None:
        self._write_u8(_MCP23017_IPOLA, val)

    @property
    def ipolb(self) -> int:
        """The raw IPOL B output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self._read_u8(_MCP23017_IPOLB)

    @ipolb.setter
    def ipolb(self, val: int) -> None:
        self._write_u8(_MCP23017_IPOLB, val)

    @property
    def interrupt_configuration(self) -> int:
        """The raw INTCON interrupt control register. The INTCON register
        controls how the associated pin value is compared for the
        interrupt-on-change feature. If  a  bit  is  set,  the  corresponding
        I/O  pin  is  compared against the associated bit in the DEFVAL
        register. If a bit value is clear, the corresponding I/O pin is
        compared against the previous value.
        """
        return self._read_u16le(_MCP23017_INTCONA)

    @interrupt_configuration.setter
    def interrupt_configuration(self, val: int) -> None:
        self._write_u16le(_MCP23017_INTCONA, val)

    @property
    def interrupt_enable(self) -> int:
        """The raw GPINTEN interrupt control register. The GPINTEN register
        controls the interrupt-on-change feature for each pin. If a bit is
        set, the corresponding pin is enabled for interrupt-on-change.
        The DEFVAL and INTCON registers must also be configured if any pins
        are enabled for interrupt-on-change.
        """
        return self._read_u16le(_MCP23017_GPINTENA)

    @interrupt_enable.setter
    def interrupt_enable(self, val: int) -> None:
        self._write_u16le(_MCP23017_GPINTENA, val)

    @property
    def default_value(self) -> int:
        """The raw DEFVAL interrupt control register. The default comparison
        value is configured in the DEFVAL register. If enabled (via GPINTEN
        and INTCON) to compare against the DEFVAL register, an opposite value
        on the associated pin will cause an interrupt to occur.
        """
        return self._read_u16le(_MCP23017_DEFVALA)

    @default_value.setter
    def default_value(self, val: int) -> None:
        self._write_u16le(_MCP23017_DEFVALA, val)

    @property
    def io_control(self) -> int:
        """The raw IOCON configuration register. Bit 1 controls interrupt
        polarity (1 = active-high, 0 = active-low). Bit 2 is whether irq pin
        is open drain (1 = open drain, 0 = push-pull). Bit 3 is unused.
        Bit 4 is whether SDA slew rate is enabled (1 = yes). Bit 5 is if I2C
        address pointer auto-increments (1 = no). Bit 6 is whether interrupt
        pins are internally connected (1 = yes). Bit 7 is whether registers
        are all in one bank (1 = no), this is silently ignored if set to ``1``.
        """
        return self._read_u8(_MCP23017_IOCON)

    @io_control.setter
    def io_control(self, val: int) -> None:
        val &= ~0x80
        self._write_u8(_MCP23017_IOCON, val)

    @property
    def int_flag(self) -> List[int]:
        """Returns a list with the pin numbers that caused an interrupt
        port A ----> pins 0-7
        port B ----> pins 8-15
        """
        intf = self._read_u16le(_MCP23017_INTFA)
        flags = [pin for pin in range(16) if intf & (1 << pin)]
        return flags

    @property
    def int_flaga(self) -> List[int]:
        """Returns a list of pin numbers that caused an interrupt in port A
        pins: 0-7
        """
        intfa = self._read_u8(_MCP23017_INTFA)
        flags = [pin for pin in range(8) if intfa & (1 << pin)]
        return flags

    @property
    def int_flagb(self) -> List[int]:
        """Returns a list of pin numbers that caused an interrupt in port B
        pins: 8-15
        """
        intfb = self._read_u8(_MCP23017_INTFB)
        flags = [pin + 8 for pin in range(8) if intfb & (1 << pin)]
        return flags

    @property
    def int_cap(self) -> List[int]:
        """Returns a list with the pin values at time of interrupt
        port A ----> pins 0-7
        port B ----> pins 8-15
        """
        intcap = self._read_u16le(_MCP23017_INTCAPA)
        return [(intcap >> pin) & 1 for pin in range(16)]

    @property
    def int_capa(self) -> List[int]:
        """Returns a list of pin values at time of interrupt
        pins: 0-7
        """
        intcapa = self._read_u8(_MCP23017_INTCAPA)
        return [(intcapa >> pin) & 1 for pin in range(8)]

    @property
    def int_capb(self) -> List[int]:
        """Returns a list of pin values at time of interrupt
        pins: 8-15
        """
        intcapb = self._read_u8(_MCP23017_INTCAPB)
        return [(intcapb >> pin) & 1 for pin in range(8)]

    def clear_ints(self) -> None:
        """Clears interrupts by reading INTCAP."""
        self._read_u16le(_MCP23017_INTCAPA)

    def clear_inta(self) -> None:
        """Clears port A interrupts."""
        self._read_u8(_MCP23017_INTCAPA)

    def clear_intb(self) -> None:
        """Clears port B interrupts."""
        self._read_u8(_MCP23017_INTCAPB)
