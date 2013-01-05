#! /bin/bash
adb root
adb uninstall com.facebook.katana > /dev/null
monkeyrunner clean.py
monkeyrunner FacebookBench.py