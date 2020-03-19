# The MIT License (MIT)
#
# Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ds1841`
================================================================================

Library for the DPS1841 I2C Logarithmic Resistor

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* Adafruit's DPS1841 Breakout: https://www.adafruit.com/product/4560

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DS1841.git"

from time import sleep
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import RWBits, ROBits


_DS1841_IVR	= 0x00
_DS1841_CR0	= 0x02
_DS1841_CR1	= 0x03
_DS1841_LUTAR	= 0x08
_DS1841_WR	= 0x09
_DS1841_CR2	= 0x0A
_DS1841_TEMP	= 0x0C
_DS1841_VOLTAGE	= 0x0E
_DS1841_LUT	= 0x80 # to C7h

_DS1841_VCC_LSB = 25.6
_DS1841_DEFAULT_ADDRESS = 0x28 # up to 0x2B

class DS1841:

    _initial_value_register = UnaryStruct(_DS1841_IVR, ">B")
    _lut_address = UnaryStruct(_DS1841_LUTAR, ">B")
    _wiper_register = UnaryStruct(_DS1841_WR, ">B")
    _control_register_0 = UnaryStruct(_DS1841_CR0, ">B")
    _control_register_1 = UnaryStruct(_DS1841_CR1, ">B")
    _control_register_2 = UnaryStruct(_DS1841_CR2, ">B")

    _temperature_register = UnaryStruct(_DS1841_TEMP, ">b")
    _voltage_register = UnaryStruct(_DS1841_VOLTAGE, ">B")

    shadow_disable = RWBit(_DS1841_CR0, 7)

    _adder_mode_bit = RWBit(_DS1841_CR1, 1)
    update_mode = RWBit(_DS1841_CR1, 0)

    _lut_address_en = RWBit(_DS1841_CR2, 1)
    wiper_access = RWBit(_DS1841_CR2, 2)
    _lut = StructArray(_DS1841_LUT, ">B", 72)

    def __init__(self, i2c_bus, address=_DS1841_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        # no good way of identifying the chip

        self.shadow_disable = True # turn off eeprom updates to IV and CR0
        # self._adder_mode_bit = False # Don't add IV to WR
        # UPDATE MODE MUST BE FALSE FOR WIPER TO SHADOW IV
        # self._update_mode_bit = True # update voltage and temp

        self._lut_address_en = True #
        self.wiper_access_bit = False # update WR by I2C
        self.lut_mode_enabled = False

    @property
    def wiper(self):
        return self._wiper_register

    @wiper.setter
    def wiper(self, value):
        if value > 127:
            raise AttributeError("wiper must be from 0-127")
        self._wiper_register = value

    @property
    def initial_value(self):
        return self._initial_value_register

    @initial_value.setter
    def initial_value(self, value):
        if value > 127:
            raise AttributeError("initial_value must be from 0-127")

        self._initial_value_register = value

    @property
    def temperature(self):
        return self._temperature_register

    @property
    def voltage(self):
        return self._voltage_register * _DS1841_VCC_LSB

    @property
    def lut_mode_enabled(self):
        return self._lut_mode_enabled

    @lut_mode_enabled.setter
    def lut_mode_enabled(self, value):
        self._lut_address_en = value
        self.update_mode = value
        self.wiper_access = not value
        self._lut_mode_enabled = value

    def set_lut(self, index, value):
        if value > 127:
            raise IndexError("set_lut value must be from 0-127")
        lut_value_byte = bytearray([value])
        self._lut[index] = lut_value_byte
        sleep(0.020)

    @property
    def look_up(self):
        if not self._lut_mode_enabled:
            raise RuntimeError("lut_mode_enabled must be equal to True to use look_up")
        return (self._lut_address-_DS1841_LUT)

    @look_up.setter
    def look_up(self, value):
        if value > 71 or value < 0:
            raise IndexError("look_up value must be from 0-71")
        self._lut_address = value+_DS1841_LUT
        sleep(0.020)

