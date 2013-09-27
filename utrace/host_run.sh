#!/bin/bash
adb shell "su -c \"echo '[adafs-stat] begin time' > /dev/kmsg; echo 0 > /sys/fs/adafs/log0/staleness_sum\""
