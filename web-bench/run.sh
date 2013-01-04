#! /bin/bash
adb root
adb uninstall com.sestet.webbench > /dev/null
monkeyrunner run.py