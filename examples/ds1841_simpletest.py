import time
import board
import busio
import adafruit_ds1841
import adafruit_debug_i2c

i2c = busio.I2C(board.SCL, board.SDA)
i2c = adafruit_debug_i2c.DebugI2C(i2c)
ds = adafruit_ds1841.DS1841(i2c)
while True:
    print("Temperature = %.2f *C"%ds.temperature)
    print("voltage:", ds.voltage, "mV")

    ds.initial_value = 0
    time.sleep(1.0)
    print("\t\tWiper 1 = %d"%ds.wiper)
    print("")
    print("\t\tInitial Value 1: = %d"%ds.initial_value)
    print("")
    ds.initial_value = 69
    time.sleep(1.0)
    print("\t\t\tWiper 2 = %d"%ds.wiper)
    print("")
    print("\t\t\tInitial Value 2: = %d"%ds.initial_value)
    print("")