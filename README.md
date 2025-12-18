# AndroidBuildozerKivySample

Sample Android application written in python using buildozer and kivy

Dependencies

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev
```

Fix Build Issue

```bash
nano .venv/pyvenv.cfg
# Change second as seen below:
include-system-site-packages = true
```

Filter Debug Logs

``` spec
android.logcat_pid_only = True
```
