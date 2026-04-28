# Kivy Sample Gallery

A broader Kivy reference project for building Android apps with Python, Kivy, and Buildozer. It keeps hot reload for desktop development, but the app itself is now structured as a multi-screen sample gallery rather than only a starter template.

## What It Demonstrates

- Buttons, labels, images, and reusable rounded components
- Layout patterns including BoxLayout, GridLayout, AnchorLayout, and Splitter
- Sliders, ProgressBar, Switch, Spinner, TextInput, CheckBox, and radio-button groups
- Popups, tabs, animations, canvas drawing, touch handling, and screen navigation
- Shared theme state and callbacks that flow between screens and back to the home dashboard

## Sample Screens

- Home dashboard with live callback state and theme switching
- Components & Layouts screen with tabs, popups, images, layouts, and splitters
- Widgets & Forms screen with controls, progress, and callback syncing
- Animation, Touch, Canvas, and About screens for focused concept demos

## Requirements

- **Ubuntu 22.04+** (tested on 22.04 and 24.04)
- **Python 3.10+**
- **Java 17** (for Android builds)

## Quick Setup

Run the setup script (installs all dependencies):

```bash
./setup.sh
```

Or set up manually:

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt install -y \
    python3-pip python3-venv python3-dev build-essential git \
    ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev \
    libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    openjdk-17-jdk
```

### Environment Variables

Add to `~/.bashrc`:

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

### Python Environment

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running

### Desktop (VS Code)

Use the **Run App** or **Run Hot Reload** tasks (Ctrl+Shift+P → Tasks: Run Task).

The home screen shows the current theme and latest callback message, so you can trigger actions in a sample screen and immediately see the shared app state update when you return.

### Desktop (Terminal)

```bash
source .venv/bin/activate
python main.py -m screen:phone_oneplus_6t,portrait,scale=0.5
```

### Build Android APK

```bash
source .venv/bin/activate
buildozer -v android debug
```

The APK will be in the `bin/` folder.

## Troubleshooting

### Cython errors on Python 3.12+

Make sure you have `Cython>=3.0.0` in requirements.txt (not the old 0.29.x).

### Java not found

Ensure JAVA_HOME is set:

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

### SDL2 errors

Install SDL2 dependencies:

```bash
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

## License

MIT
