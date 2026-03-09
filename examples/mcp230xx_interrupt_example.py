# SPDX-FileCopyrightText: 2026 James Douglas
#
# SPDX-License-Identifier: MIT
#
# Demo of using the interrupt configuration registers of the MCP2300xx
# and the functionality of the interrupt pin.
#
# Example assumes the interrupt pin of the MCP2300xx is connected to
# GP15 on a Raspberry Pi Pico or similar board.
#
# Author: James Douglas

import asyncio

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23008 import MCP23008

# from adafruit_mcp230xx.mcp23017 import MCP23017

# I2C setup
i2c = busio.I2C(board.GP5, board.GP4)

# Chip setup
mcp = MCP23008(i2c)  # MCP23008
# mcp = MCP23017(i2c)  # MCP23017
# mcp = MCP23017(i2c, address=0x21)  # e.g. MCP23017 w/ A0 set

# List of all the pins (e.g. 0-7 for MCP23008, 0-15 for MCP23017)
pins = []
for pin in range(0, 8):
    pins.append(mcp.get_pin(pin))

# Set all the pins to input w/ Pull-Up
for pin in pins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP


# Setup Initial Interrupt config on MCP230xx
mcp.interrupt_enable = 0xFF  # Enable Interrupts in all pins - 0xFFFF for MCP23017
mcp.interrupt_configuration = 0x00  # interrupt on any change - 0x0000 for MCP23017
mcp.io_control = 0x04  # Open-drain INT pin
mcp.clear_ints()

# Setup interrupt listener on Pico
int_listener = digitalio.DigitalInOut(board.GP15)
int_listener.direction = digitalio.Direction.INPUT
int_listener.pull = digitalio.Pull.UP


async def monitor_interrupts():
    """
    Loop that monitors the interrupt pin and prints out the interrupt
    flags and values when an interrupt occurs.
    """
    print("Listening for MCP200xx interrupts...")

    while True:
        # The interrupt pin is open-drain and pulled UP
        # so it goes LOW on interrupt
        if not int_listener.value:
            # Identify which pin(s) caused the interrupt
            flags = mcp.int_flag
            # Capture the state of all pins at the time of the interrupt
            # Reading INTCAP also clears the interrupt flags
            caps = mcp.int_cap

            # Alternatively, you could ignore INTCAP and
            # just read the current pin states from GPIO

            if flags:
                print("\n--- Interrupt Detected ---")
                for pin in flags:
                    print(f"Pin {pin} triggered the interrupt. Captured value: {caps[pin]}")

            # We don't need to manually clear the interrupt flags,
            # reading the int_cap register already does that.
            # However, if you want to clear any pending interrupts without
            # reading the captured values (e.g. you are reading GPIO
            # directly), you can call mcp.clear_ints()

            # Add a small delay to act as a software debounce
            await asyncio.sleep(0.2)

        # Yield control back to the event loop
        await asyncio.sleep(0.01)


async def main():
    """
    Main async function to run the interrupt monitoring loop.

    Could also include other async tasks here if needed instead of
    just awaiting monitor_interrupts()
    """
    await monitor_interrupts()


# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
