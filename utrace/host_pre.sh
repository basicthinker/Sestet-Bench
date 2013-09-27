#!/bin/bash

SH_DIR=/data/data/adafs
DATA_DIR=/sdcard/adafs

if [ $# -ne 2 ]; then
	echo "Usage: $0 AppAlias OutputDir"
	exit 1
fi

app=$1
out_dir=$2
mkdir -p $2
timestamp=`date +"%F-%T"`

adb shell "su -c '$SH_DIR/dev_pre.sh $app eafs'"
adb shell "su -c '$SH_DIR/ev_trace.o'" > $out_dir/$app-ev-$timestamp.log &
adb shell "su -c 'cat /proc/kmsg | grep adafs'" > $out_dir/$app-kern-$timestamp.log &
