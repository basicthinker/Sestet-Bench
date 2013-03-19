# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

# Wrapper function for touching a point down and up
def touchDownUp(x_rate, y_rate, interval = 1):
    MonkeyRunner.sleep(interval)
    x = int(width * x_rate)
    y = int(height * y_rate)
    device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
    return

def dragVertically(y1_rate, y2_rate, duration = 0.1, steps = 5):
    x = int(width * 0.5)
    y1 = int(height * y1_rate)
    y2 = int(height * y2_rate)
    device.drag((x, y1), (x, y2), duration, steps)
    return

def takeSnapshot(x_rate, y_rate, w_rate, h_rate):
    x = int(width * x_rate)
    y = int(height * y_rate)
    w = int(width * w_rate)
    h = int(height * h_rate)
    return device.takeSnapshot().getSubImage((x, y, w, h))

def operateRR():
    #touchDownUp(0.86, 0.94) # login
    #touchDownUp(0.5, 0.19)
    #device.type('renjinglei@163.com')
    #touchDownUp(0.5, 0.27)
    #device.type('J8d5b324')
    #touchDownUp(0.5, 0.36)
    touchDownUp(0.5, 0.86, 2) # start

    touchDownUp(0.28, 0.08, 2)
    touchDownUp(0.5, 0.26)

    last = takeSnapshot(0.3, 0.35, 0.4, 0.1)
    while True:
        for i in range(10):
            dragVertically(0.9, 0.23)
        now = takeSnapshot(0.3, 0.35, 0.4, 0.1)
        if now.sameAs(last):
            break
        else:
            last = now
    return

# Main
operateRR()
print "Finished."

