# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

APK_PATH = 'baiduditu.apk'
IMAGE_PATH = './'
PKG_NAME = 'com.baidu.BaiduMap'
ACTIVITY = 'com.baidu.BaiduMap.map.mainmap.MainMapActivity'
CLEAR = False

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

# Wrapper function for touching a point down and up
def touchDownUp(x_rate, y_rate, interval = 0.6):
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

def recordTarget(index, interval = 3):
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
  
  # touches the input box
  touchDownUp(0.4, 0.08, 5)
  # inputs place
  MonkeyRunner.sleep(2)
  device.type("Tsinghua")
  begin = time.time()
  MonkeyRunner.sleep(3)
  
  # [0] origin
  index = 0
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
    touchDownUp(0.92, 0.83, 0.2)
  
  MonkeyRunner.sleep(0.2)
  for i in range(6):
    index += 1
    touchDownUp(0.92, 0.83, 0)
    waitToFinish(index, init)
    print " %d\t%f" % (index, time.time() - begin)
  
  if not init:
    print "[Sestet] \t%f" % (begin - g_begin)
  
  MonkeyRunner.sleep(5)
  device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
  touchDownUp(0.85, 0.84)
  touchDownUp(0.2, 0.6)
  return

# Main
# This version assumes that BaiduMap has been installed and configured.

if CLEAR:
  print "Bakcup current config and data."
  device.shell('mkdir -p /data/data/com.baidu.BaiduMap.bak')
  device.shell('mkdir -p /sdcard/BaiduMap.bak')
  device.shell('busybox cp -r /data/data/com.baidu.BaiduMap/* /data/data/com.baidu.BaiduMap.bak/')
  device.shell('busybox cp -r /sdcard/BaiduMap/* /sdcard/BaiduMap.bak/')
else:
  print "Restore former config and data."
  device.shell('rm -r /data/data/com.baidu.BaiduMap/*')
  device.shell('rm -r /sdcard/BaiduMap/*')
  device.shell('busybox cp -r /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
  device.shell('busybox cp -r /sdcard/BaiduMap.bak/* /sdcard/BaiduMap/')
  device.shell('chmod -R 777 /data/data/com.baidu.BaiduMap')
  device.shell('chmod -R 777 /sdcard/BaiduMap')

operateMap(True)

print "Main begins."
g_begin = time.time()

for i in range(12):
  print "Trial %d:" % (i)
  
  if i % 2 == 0:
    # clear and copy
    device.shell('rm -r /data/data/com.baidu.BaiduMap/*')
    device.shell('rm -r /sdcard/BaiduMap/*')
    device.shell('busybox cp -r /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
    device.shell('busybox cp -r /sdcard/BaiduMap.bak/* /sdcard/BaiduMap/')
    device.shell('chmod -R 777 /data/data/com.baidu.BaiduMap')
    device.shell('chmod -R 777 /sdcard/BaiduMap')
    MonkeyRunner.sleep(2)
    operateMap()
    MonkeyRunner.sleep(2)
  else:
    device.shell('mount -t ramfs none /data/data/com.baidu.BaiduMap')
    device.shell('mount -t ramfs none /sdcard/BaiduMap')
    device.shell('busybox cp -r /data/data/com.baidu.BaiduMap.bak/* /data/data/com.baidu.BaiduMap/')
    device.shell('busybox cp -r /sdcard/BaiduMap.bak/* /sdcard/BaiduMap/')
    device.shell('chmod -R 777 /data/data/com.baidu.BaiduMap')
    device.shell('chmod -R 777 /sdcard/BaiduMap')
    MonkeyRunner.sleep(2)
    operateMap()
    MonkeyRunner.sleep(2)
    device.shell('busybox fuser -mk /data/data/com.baidu.BaiduMap')
    device.shell('busybox fuser -mk /sdcard/BaiduMap')
    device.shell('umount /data/data/com.baidu.BaiduMap')
    device.shell('umount /sdcard/BaiduMap')

if CLEAR:
  device.shell('rm -r /data/data/com.baidu.BaiduMap')
  device.shell('rm -r /sdcard/BaiduMap')
else:
  print "Latest data are reserved."

