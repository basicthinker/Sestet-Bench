from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import time

APK_PATH = 'webbench.apk'
PKG_NAME = 'com.sestet.webbench'
PKG_NAME_BAK = PKG_NAME + '.bak'
ACTIVITY = '.MainActivity'

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
# retrives basic properties
width = int(device.getProperty("display.width"))
height = int(device.getProperty("display.height"))

def takeSnapshot(x_rate, y_rate, w_rate, h_rate):
  x = int(width * x_rate)
  y = int(height * y_rate)
  w = int(width * w_rate)
  h = int(height * h_rate)
  return device.takeSnapshot().getSubImage((x, y, w, h))

def waitToFinish(x_rate, y_rate, w_rate, h_rate, interval = 5):
  target = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
  MonkeyRunner.sleep(interval)
  state = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
  while (not target.sameAs(state)):
    target = state
    MonkeyRunner.sleep(interval)
    state = takeSnapshot(x_rate, y_rate, w_rate, h_rate)
  return state

def operateWeb():
  # Launches the app
  runComponent = PKG_NAME + '/' + ACTIVITY
  device.startActivity(component=runComponent)
  waitToFinish(0, 0.05, 1, 0.2)
  return

# Main
begin = time.time()
check = device.shell('cd /data/data/' + PKG_NAME_BAK)
if check.find('can\'t') >= 0:
  device.shell('mkdir /data/data/' + PKG_NAME_BAK)

for i in range(12):
  print "Trial %d:" % (i + 1)
  check = device.shell('cd /data/data/' + PKG_NAME)
  if check.find('can\'t') < 0:
    print "Error: installation directory exists."
    sys.exit(-1)
  
  if i % 2 == 0:
    device.installPackage(APK_PATH)
    MonkeyRunner.sleep(10)
    start = time.time() - begin 
    operateWeb()
    end = time.time() - begin
    print "\t%fs - %fs" % (start, end)
    device.removePackage(PKG_NAME)
  else:
    device.shell('mkdir /data/data/' + PKG_NAME)
    device.shell('mount -t ramfs none /data/data/' + PKG_NAME)
    device.installPackage(APK_PATH)
    MonkeyRunner.sleep(10)
    start = time.time() - begin 
    operateWeb()
    end = time.time() - begin
    print "\t%fs - %fs" % (start, end)
    device.removePackage(PKG_NAME)
    MonkeyRunner.sleep(2)
    device.shell('busybox fuser -mk /data/data/' + PKG_NAME)
    device.shell('umount /data/data/' + PKG_NAME)
    device.shell('rmdir /data/data/' + PKG_NAME)

device.shell('rmdir /data/data/' + PKG_NAME_BAK)