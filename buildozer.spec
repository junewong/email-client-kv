[app]
title = Kivy Build Test
package.name = kivytest
package.domain = com.test
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy
permissions = 
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a
