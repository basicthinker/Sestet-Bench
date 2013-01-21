# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

APK_PATH = 'baiduditu.apk'
IMAGE_PATH = './'
PKG_NAME = 'com.baidu.BaiduMap'
ACTIVITY = 'com.baidu.BaiduMap.map.mainmap.MainMapActivity'
SATELLITE = False

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

NUM_SNAP = 11
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

def finishOperation(index, threshod = 0.95, interval = 0.2):
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
  
  if SATELLITE:
    MonkeyRunner.sleep(0.5)
    device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
    touchDownUp(0.14, 0.73)
    MonkeyRunner.sleep(0.5)
    touchDownUp(0.5, 0.2)
  
  print "20 seconds for your check."
  MonkeyRunner.sleep(20)
  
  # touches the input box
  touchDownUp(0.4, 0.08, 4)
  # inputs place
  MonkeyRunner.sleep(3)
  device.type("Tsinghua")
  MonkeyRunner.sleep(5)
  
  # [0] origin
  index = 0
  begin = time.time()
  touchDownUp(0.9, 0.17, 0)
  waitToFinish(index, init)
  print " %d\t%f" % (index, time.time() - begin)
  
  # zoom in
  index += 1
  for i in range(3):
    touchDownUp(0.92, 0.76, 0.5)
  waitToFinish(index, init)
  print " %d\t%f" % (index, time.time() - begin)
  
  for i in range(4):
    # restore
    touchDownUp(0.92, 0.83, 0.5)
  
  for i in range(6):
    index += 1
    touchDownUp(0.92, 0.83)
    waitToFinish(index, init)
    print " %d\t%f" % (index, time.time() - begin)
  
  if not init:
    print "[Sestet] \t%f" % (begin - g_begin)
  
  device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
  touchDownUp(0.85, 0.84)
  touchDownUp(0.2, 0.33)
  MonkeyRunner.sleep(5)
  return

# Main
# This version assumes that BaiduMap has been installed and configured.
check = device.shell('cd /data/data/com.baidu.BaiduMap')
if check.find('can\'t') > 0:
  device.installPackage(APK_PATH)
  print "Two minutes for your config."
  MonkeyRunner.sleep(120)

operateMap(True)

print "Main begins."
g_begin = time.time()

for i in range(12):
  print "Trial %d:" % (i)
  
  if i % 2 == 0:
    device.shell('rm -r /data/data/com.baidu.BaiduMap/*')
    device.shell('cp -r /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
    device.shell('chmod -R a+rwx /data/data/com.baidu.BaiduMap')
    operateMap()
  else:
    device.shell('mount -t ramfs none /data/data/com.baidu.BaiduMap')
    device.shell('chmod a+rwx /data/data/com.baidu.BaiduMap')
    device.shell('cp -r /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
    device.shell('chmod -R a+rwx /data/data/com.baidu.BaiduMap')
    operateMap()
    MonkeyRunner.sleep(1)
    device.shell('busybox fuser -mk /data/data/com.baidu.BaiduMap')
    device.shell('umount /data/data/com.baidu.BaiduMap')
