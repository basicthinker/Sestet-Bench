# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

APK_PATH = 'baiduditu.apk'
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

NUM_SNAP = 11
targets = [None] * NUM_SNAP

def takeSnapshot():
  y = height * 0.05
  h = height * 0.90
  return device.takeSnapshot().getSubImage((0, y, width, h))

def waitToFinish(threshold = 0.95, interval = 0.2):
  MonkeyRunner.sleep(interval)
  target = takeSnapshot()
  MonkeyRunner.sleep(interval)
  state = takeSnapshot()
  while (not target.sameAs(state)):
    target = state
    MonkeyRunner.sleep(interval)
    state = takeSnapshot()
  return

def operateMap():
  # Launches the app
  #runComponent = PKG_NAME + '/' + ACTIVITY
  #device.startActivity(component=runComponent)
  
  # touches the input box
  touchDownUp(0.4, 0.08, 4)
  # inputs place
  MonkeyRunner.sleep(2)
  device.type("Tsinghua")
  MonkeyRunner.sleep(3)
  
  touchDownUp(0.9, 0.17, 0)
  waitToFinish()
  
  # zoom in
  for i in range(3):
    touchDownUp(0.92, 0.76, 0.5)
  waitToFinish()
  
  for i in range(4):
    # restore
    touchDownUp(0.92, 0.83, 0.5)
  
  for i in range(6):
    touchDownUp(0.92, 0.83)
    waitToFinish()
  
  #device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
  #touchDownUp(0.85, 0.84)
  #touchDownUp(0.2, 0.6)
  print "Finished."
  return

# Main
# This version assumes that BaiduMap has been installed and configured.

operateMap()


