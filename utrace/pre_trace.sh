#!/bin/bash

SH_DIR=/data/data/rffs
DATA_DIR=/sdcard/rffs

if [ $# -ne 2 ]; then
	echo "Usage: $0 AppAlias OutputDir"
	exit 1
fi

app_alias=$1
out_dir=$2
timestamp=`date +"%F-%T"`

adb shell "su -c '$SH_DIR/prepare_in_dev.sh $DATA_DIR/$app_alias.part $DATA_DIR/rffs.ko'"
adb shell "su -c '$SH_DIR/ev_trace.o'" > $app_alias-ev-$timestamp.log &
adb shell "su -c 'cat /proc/kmsg | grep rffs'" > $app_alias-kern-$timestamp.log &
adb shell "su -c 'echo "[rffs] begin time" > /dev/kmsg; $SH_DIR/cpu_trace.o 5 0'" > $app_alias-cpu-$timestamp.log &
cat $app_alias-cpu-$timestamp.log
