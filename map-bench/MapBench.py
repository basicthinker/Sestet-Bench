# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

APK_PATH = '/Users/stone/Projects/Sestet-Bench/map-bench/baiduditu.apk'
IMAGE_PATH = '/Users/stone/Projects/Sestet-Bench/map-bench/'
PKG_NAME = 'com.baidu.BaiduMap'
ACTIVITY = 'com.baidu.BaiduMap.map.mainmap.MainMapActivity'

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

# Wrapper function for touching a point down and up
def touchDownUp(x_rate, y_rate, interval = 0.5):
    MonkeyRunner.sleep(interval)
    x = int(width * x_rate)
    y = int(height * y_rate)
    device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
    return

NUM_SNAP = 12
targets = [None] * NUM_SNAP

def takeSnapshot():
    y = height * 0.05
    h = height * 0.90
    return device.takeSnapshot().getSubImage((0, y, width, h))

def recordTarget(index, interval = 5):
    MonkeyRunner.sleep(interval)
    targets[index] = takeSnapshot()
    MonkeyRunner.sleep(interval)
    state = takeSnapshot()
    while (not targets[index].sameAs(state)):
        targets[index] = state
        MonkeyRunner.sleep(interval)
        state = takeSnapshot()
    state.writeToFile(IMAGE_PATH + 'MapBenchSnapshot' + str(index) + '.png') 
    return

def finishOperation(index, threshod = 0.96, interval = 0.5):
    MonkeyRunner.sleep(interval)
    state = takeSnapshot()
    while (not targets[index].sameAs(state, threshod)):
        MonkeyRunner.sleep(interval)
        state = takeSnapshot()
    return

def waitToFinish(index, init):
    if init:
        recordTarget(index)
    else:
        finishOperation(index)
    return


def operateMap(init=False):
    # Launches the app
    runComponent = PKG_NAME + '/' + ACTIVITY
    device.startActivity(component=runComponent)
    # accepts TOS
    touchDownUp(0.3, 0.85, 2)
    # closes welcome
    touchDownUp(0.96, 0.07, 1)
    # cancels further setting
    touchDownUp(0.76, 0.48, 1)
    # turns off the real traffic
    touchDownUp(0.92, 0.17, 2)
    # touches the input box
    touchDownUp(0.4, 0.08, 1)
    # inputs place
    MonkeyRunner.sleep(2)
    device.type("Tsinghua")

    # [0] origin
    index = 0
    touchDownUp(0.9, 0.17)
    begin = time.time()
    waitToFinish(index, init)
    print "[Sestet] %d\t%f" % (index, time.time() - begin)

    for i in range(4):
        # zoom in
        index += 1
        touchDownUp(0.92, 0.76, 0)
        waitToFinish(index, init)
        print "[Sestet] %d\t%f" % (index, time.time() - begin)

    for i in range(4):
        # restore
        touchDownUp(0.92, 0.83)

    for i in range(7):
        index += 1
        touchDownUp(0.92, 0.83)
        waitToFinish(index, init)
        print "[Sestet] %d\t%f" % (index, time.time() - begin)

# Main
device.installPackage(APK_PATH)
operateMap(True)
device.removePackage(PKG_NAME)

for i in range(6):
    print "Trial %d:" % (i)
    check = device.shell('cd /data/data/com.baidu.BaiduMap')
    if check.find('can\'t') < 0:
        sys.exit("Error: %d" % check.find('can\'t'))

    if i % 2 == 0:
        device.installPackage(APK_PATH)
        MonkeyRunner.sleep(2)
        operateMap()
        device.removePackage(PKG_NAME)
    else:
        device.installPackage(APK_PATH)
        MonkeyRunner.sleep(2)
        device.shell('mv /data/data/com.baidu.BaiduMap/* /data/data/com.baidu.BaiduMap.bak/')
        device.shell('mount -t ramfs none /data/data/com.baidu.BaiduMap')
        device.shell('chmod a+rwx /data/data/com.baidu.BaiduMap')
        device.shell('mv /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
        operateMap()
        device.removePackage(PKG_NAME)
        MonkeyRunner.sleep(1)
        device.shell('busybox fuser -mk /data/data/com.baidu.BaiduMap')
        device.shell('umount /data/data/com.baidu.BaiduMap')
        device.shell('rmdir /data/data/com.baidu.BaiduMap')


