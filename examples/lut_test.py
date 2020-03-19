import time
import board
import busio
import adafruit_ds1841
import adafruit_debug_i2c

# def settings(ds):
#     ctrl1 = ds._control_register_1
#     ctrl2 = ds._control_register_2

#     update_mode = ctrl1 & 0x1 > 0
#     adder_mode = ctrl1 & 0x2 > 0

#     lutar = ctrl2 & 0x2 > 0
#     wiper_access = ctrl2 & 0x4 > 0

#     print("Update Mode:", update_mode, "Adder Mode:", adder_mode, "Lutar:", lutar, "Wiper Access:", wiper_access)

i2c = busio.I2C(board.SCL, board.SDA)
i2c = adafruit_debug_i2c.DebugI2C(i2c)
ds = adafruit_ds1841.DS1841(i2c)
# settings(ds)
# while True:

#     print("Temperature = %.2f *C"%ds.temperature)
#     print("voltage:", ds.voltage, "mV")

#     ds.initial_value = 0
#     time.sleep(1.0)
#     print("\t\tWiper 1 = %d"%ds.wiper)
#     print("")
#     print("\t\tInitial Value 1: = %d"%ds.initial_value)
#     print("")
#     ds.initial_value = 69
#     time.sleep(1.0)
#     print("\t\t\tWiper 2 = %d"%ds.wiper)
#     print("")
#     print("\t\t\tInitial Value 2: = %d"%ds.initial_value)
#     print("")