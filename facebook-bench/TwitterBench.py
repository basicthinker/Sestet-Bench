# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

PKG_NAME = 'com.twitter.'
ACTIVITY = '.LoginActivity'

DEV_PRE_SCRIPT = '/data/data/adafs/dev_pre.sh facebook'
DEV_CLEAR_SCRIPT = '/data/data/adafs/dev_clear.sh facebook'

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

# Wrapper function for touching a point down and up
def touchDownUp(x_rate, y_rate, interval = 0.2):
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

def waitToFinish(x_rate, y_rate, w_rate, h_rate, interval = 0.2):
    target = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
    MonkeyRunner.sleep(interval)
    state = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
    while (not target.sameAs(state)):
        target = state
        MonkeyRunner.sleep(interval)
        state = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
    return state

def operateFB():
    # Launches the app
    runComponent = PKG_NAME + '/' + ACTIVITY
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(8)
    waitToFinish(0.4, 0.4, 0.2, 0.2, 4)
  
    begin = time.time()
    for t in range(5):
        for i in range(5):
            dragVertically(0.9, 0.23)
        waitToFinish(0.3, 0.89, 0.4, 0.1, 0.2)
        print "[Sestet] \t%d \t%f" % (t + 1, time.time() - begin)
    end = time.time()
    print "[Sestet] \t%f \t%f" % (begin - g_begin, end - g_begin)
    MonkeyRunner.sleep(5)
    return

# Main
print "Main begins."
g_begin = time.time()

for i in range(2):
    print "Trial %d:" % (i + 1)
    if i % 2 == 0:
        device.shell('su -c ' + DEV_PRE_SCRIPT + ' ext4')
        operateFB()
        device.shell('su -c ' + DEV_CLEAR_SCRIPT + ' ext4')
    else:
        device.shell('su -c ' + DEV_PRE_SCRIPT + ' eafs')
        operateFB()
        device.shell('su -c ' + DEV_CLEAR_SCRIPT + ' eafs')

