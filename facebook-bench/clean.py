from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys

PKG_NAME = 'com.facebook.katana'
PKG_NAME_BAK = PKG_NAME + '.bak'

device = MonkeyRunner.waitForConnection()

check = device.shell('cd /data/data/' + PKG_NAME)
if check.find('can\'t') < 0:
    device.shell('busybox fuser -k /data/data/' + PKG_NAME)
    device.shell('umount /data/data/' + PKG_NAME)
    device.shell('rmdir /data/data/' + PKG_NAME)
device.shell('rmdir /data/data/' + PKG_NAME_BAK)