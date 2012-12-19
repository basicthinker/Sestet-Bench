# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

APK_PATH = 'C:\\Users\\basicthinker\\Downloads\\com.baidu.BaiduMap-1.apk'
IMAGE_PATH = 'C:\\Users\\basicthinker\\Downloads\\'
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

NUM_SNAP = 10
targets = [None] * NUM_SNAP # [0]origin, [1]zoom-in 1, [2]zoom-in 2, [3]zoom-in 3,
                            # [4]move-right, [5]move-down, [6]move-left, [7]move-up
                            # [8]zoon-out 1, [9]zoom-out 2, [10]zoom-out 3

def takeSnapshot():
    y = height * 0.05
    h = height * 0.90
    return device.takeSnapshot().getSubImage((0, y, width, h))

def recordTarget(index, interval = 10):
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

def finishOperation(index, threshod = 0.5, interval = 5):
    MonkeyRunner.sleep(interval)
    state = takeSnapshot()
    while (not targets[index].sameAs(state, threshod)):
        state.writeToFile(IMAGE_PATH + 'MapBenchSnapshot' + str(index) + 'x.png')
        MonkeyRunner.sleep(interval)
        state = takeSnapshot()
    return

def operateMap(init=False):
    # Launches the app
    runComponent = PKG_NAME + '/' + ACTIVITY
    device.startActivity(component=runComponent)
    # accepts TOS
    touchDownUp(0.3, 0.85)
    # closes welcome
    touchDownUp(0.96, 0.07)
    # cancels further setting
    touchDownUp(0.76, 0.48)
    # turns off the real traffic
    touchDownUp(0.92, 0.17, 1)
    # touches the input box
    touchDownUp(0.4, 0.08)
    # inputs place
    MonkeyRunner.sleep(3)
    device.type("Tsinghua")

    touchDownUp(0.9, 0.17)
    index = 0; # [0] origin
    if init:
        recordTarget(index)
    else:
        finishOperation(index)
    return

# Main
device.removePackage(PKG_NAME)
device.installPackage(APK_PATH)
operateMap(True)

device.removePackage(PKG_NAME)
device.installPackage(APK_PATH)
operateMap()


