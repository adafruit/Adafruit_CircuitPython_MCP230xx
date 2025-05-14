Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp230xx/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/mcp230xx/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython module for the MCP23017/08 I2C and MCP23S17/08 SPI I/O extenders.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mcp230xx/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mcp230xx

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mcp230xx

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-mcp230xx

Usage Example
=============

See examples/mcp230xx_simpletest.py for a demo of the usage.

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/mcp230xx/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Warning
=======
Some people have reported an undocumented bug that can potentially corrupt the I2C bus.
It occurs if an MCP230XX input pin state changes during I2C readout. **This should be very rare.** For more information, see this `forum post <https://www.microchip.com/forums/m646539.aspx>`_ and this `knowledge base article <https://microchipsupport.force.com/s/article/On-MCP23008-MCP23017-SDA-line-change-when-GPIO7-input-change>`_ .

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
