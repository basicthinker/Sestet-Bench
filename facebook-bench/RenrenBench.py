# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import sys

APK_PATH = 'renren.apk'
PKG_NAME = 'com.renren.mobile.android'
ACTIVITY = 'com.renren.mobile.android.ui.WelcomeScreen'

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

def dragVertically(y1_rate, y2_rate, duration = 0.1, steps = 2):
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
    # Launches the app
    runComponent = PKG_NAME + '/' + ACTIVITY
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(5)
  
    touchDownUp(0.86, 0.94) # login
    touchDownUp(0.5, 0.146)
    device.type('renjinglei@163.com')
    touchDownUp(0.5, 0.29)
    device.type('J8d5b324')
    touchDownUp(0.5, 0.38)
    touchDownUp(0.5, 0.85, 2) # start

    touchDownUp(0.3, 0.08, 2)
    touchDownUp(0.5, 0.28)

    begin = time.time()
    last = takeSnapshot(0.3, 0.35, 0.4, 0.1)
    while True:
        for i in range(5):
            dragVertically(0.9, 0.23)
        print "  %f" % (time.time() - begin)
        now = takeSnapshot(0.3, 0.35, 0.4, 0.1)
        if now.sameAs(last):
            break
        else:
            last = now
    print "[Sestet] \t%f" % (begin - g_begin)
    MonkeyRunner.sleep(5)
    return

# Main
print "Main begins."
g_begin = time.time()
PKG_NAME_BAK = PKG_NAME + '.bak'
device.shell('rmdir /data/data/' + PKG_NAME)
check = device.shell('cd /data/data/' + PKG_NAME_BAK)
if check.find('can\'t') >= 0:
    device.shell('mkdir /data/data/' + PKG_NAME_BAK)

for i in range(8):
    print "Trial %d:" % (i + 1)
    check = device.shell('cd /data/data/' + PKG_NAME)
    if check.find('can\'t') < 0:
        print 'Error: installation directory exists.'
        sys.exit(-1)

    if i % 2 == 0:
        device.installPackage(APK_PATH)
        MonkeyRunner.sleep(1)
        operateRR()
        device.removePackage(PKG_NAME)
        MonkeyRunner.sleep(1)
        device.shell('rmdir /data/data/' + PKG_NAME)
    else:
        device.installPackage(APK_PATH)
        MonkeyRunner.sleep(1)
        device.shell('mv /data/data/' + PKG_NAME + '/* /data/data/' + PKG_NAME_BAK)
        device.shell('mount -t ramfs none /data/data/' + PKG_NAME)
        device.shell('chmod a+rwx /data/data/' + PKG_NAME)
        device.shell('mv /data/data/' + PKG_NAME_BAK + '/* /data/data/' + PKG_NAME)
        operateRR()
        device.removePackage(PKG_NAME)
        MonkeyRunner.sleep(1)
        device.shell('busybox fuser -mk /data/data/' + PKG_NAME)
        device.shell('umount /data/data/' + PKG_NAME)
        device.shell('rmdir /data/data/' + PKG_NAME)

device.shell('rmdir /data/data/' + PKG_NAME_BAK)


