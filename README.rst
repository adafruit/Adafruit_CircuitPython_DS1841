Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ds1841/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ds1841/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_DS1841/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_DS1841/actions
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython library for the Maxim DS1841 I2C Logarithmic Resistor


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ds1841/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ds1841

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ds1841

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-ds1841

Usage Example
=============

.. code-block:: python

    from time import sleep
    import board
    import busio
    import adafruit_ds1841
    from analogio import AnalogIn

    ####### NOTE ################
    # this example will not work with Blinka/rasberry Pi due to the lack of analog pins.
    # Blinka and Raspberry Pi users should run the "ds1841_blinka_simpletest.py" example

    # WIRING:
    # 1 Wire connecting  VCC to RH to make a voltage divider using the
    #   internal resistor between RH and RW
    # 2 Wire connecting RW to A0

    i2c = busio.I2C(board.SCL, board.SDA)
    ds1841 = adafruit_ds1841.DS1841(i2c)
    wiper_output = AnalogIn(board.A0)

    while True:

        ds1841.wiper = 127
        print("Wiper set to %d"%ds1841.wiper)
        voltage = wiper_output.value
        voltage *= 3.3
        voltage /= 65535
        print("Wiper voltage: %.2f"%voltage)
        print("")
        sleep(1.0)

        ds1841.wiper = 0
        print("Wiper set to %d"%ds1841.wiper)
        voltage = wiper_output.value
        voltage *= 3.3
        voltage /= 65535
        print("Wiper voltage: %.2f"%voltage)
        print("")
        sleep(1.0)

        ds1841.wiper = 63
        print("Wiper set to %d"%ds1841.wiper)
        voltage = wiper_output.value
        voltage *= 3.3
        voltage /= 65535
        print("Wiper voltage: %.2f"%voltage)
        print("")
        sleep(1.0)


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ds1841/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_DS1841/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
