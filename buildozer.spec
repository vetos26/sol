[app]
title = Calculator
package.name = calculator
package.domain = org.vetos26

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = tests,.venv
version = 0.1.0

# The interface uses Kivy directly; KivyMD is not needed in the APK.
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
