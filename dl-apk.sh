#!/bin/bash

cd ./dist/ && gh run download -n app-debug && adb uninstall com.example.mailclient 2>/dev/null; adb install app-debug.apk
