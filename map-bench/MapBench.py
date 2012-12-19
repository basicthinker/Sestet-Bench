# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

# sets a variable with the package's internal name
package = 'com.baidu.BaiduMap'
# sets a variable with the name of an Activity in the package
activity = 'com.baidu.BaiduMap.map.mainmap.MainMapActivity'
# sets the name of the component to start
runComponent = package + '/' + activity

# Runs the component
device.startActivity(component=runComponent)
MonkeyRunner.sleep(0.5)
# device.shell("adb shell am start -n com.baidu.BaiduMap/com.baidu.BaiduMap.map.mainmap.MainMapActivity");

# Touches the input box
x = int(width * 0.4)
y = int(height * 0.08)
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(1)

# Inputs place and search
device.type("Tsinghua")
x = int(width * 0.9)
y = int(height * 0.17)
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)

# Initial image
MonkeyRunner.sleep(10)
snapshot = device.takeSnapshot()

# Presses the Menu button
# device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
