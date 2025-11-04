[app]
title = 邮件客户端
package.name = mailclient
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0
permissions = INTERNET
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
android.skip_update = False
android.sdk_path = ~/.buildozer/android/platform/android-sdk
