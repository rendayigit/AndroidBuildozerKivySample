# Kivy Android App Template 🚀

A sample template project for developing Android applications using **Python**, **Kivy**, and **Buildozer**. Features hot reload support for rapid development on desktop.

## ✨ Features

- **Multi-screen navigation** with smooth transitions
- **Animation demos** - bounce, spin, color cycling
- **Widget showcase** - sliders, switches, spinners, text inputs, progress bars
- **Touch interaction** demo with visual feedback
- **Canvas drawing** with shapes and transforms
- **Hot reload** support for desktop development (via Kaki)
- **Pre-configured VS Code** tasks and launch configurations

## 📁 Project Structure

```bash
├── main.py              # App entry point (Android vs Desktop handling)
├── app_logic.py         # Python logic for all screens
├── app_logic.kv         # Main KV file (imports screen KV files)
├── screens/             # Individual screen KV files
│   ├── home.kv          # Home/navigation screen
│   ├── animation.kv     # Animation demo screen
│   ├── widgets.kv       # Widget showcase screen
│   ├── touch.kv         # Touch interaction screen
│   ├── canvas.kv        # Canvas drawing screen
│   └── about.kv         # About screen
├── buildozer.spec       # Android build configuration
├── requirements.txt     # Python dependencies
└── .vscode/
    ├── tasks.json       # Build & run tasks
    ├── launch.json      # Debug configurations
    └── settings.json    # Editor settings
```

## 🛠️ Prerequisites

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf \
    libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev
```

### Python Environment

```bash
# Create virtual environment (include system site packages)
# This sets `include-system-site-packages = true` in `.venv/pyvenv.cfg`.
python3 -m venv .venv --system-site-packages
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Fix Build Issue (if needed)

If you encounter build issues, enable system site packages:

```bash
nano .venv/pyvenv.cfg
# Change to:
include-system-site-packages = true
```

## 🚀 Running the App

### Desktop (with Hot Reload)

Use VS Code tasks or run directly:

```bash
# Standard run
.venv/bin/python main.py -m screen:phone_oneplus_6t,portrait,scale=0.3

# With hot reload (auto-refreshes on file changes)
DEBUG=1 .venv/bin/python main.py -m screen:phone_oneplus_6t,portrait,scale=0.3
```

### VS Code Tasks

- **Run App** - Launch the app with phone screen emulation
- **Run Hot Reload** - Launch with auto-reload on file changes
- **Build App** - Build Android APK
- **Clean Build** - Clean and rebuild Android APK
- **Install & Run on Phone** - Deploy to connected Android device

### Debugging

Use the VS Code launch configurations (F5):

- **Python: Run App (Desktop)** - Debug with screen emulation
- **Python: Run App with Hot Reload** - Debug with hot reload
- **Python: Debug Current File** - Debug the active file
- **Python: Attach to Remote** - Attach to running Android app (requires debugpy)

## 📱 Building for Android

### First Time Setup

The `buildozer.spec` file is pre-configured. Key settings you may want to modify:

```spec
# App identity
title = My Application
package.name = myapp
package.domain = org.test

# Version
version = 0.1

# Requirements (add more as needed)
requirements = python3,kivy

# Permissions (uncomment as needed)
#android.permissions = android.permission.INTERNET

# Filter logs to your app only
android.logcat_pid_only = True
```

### Build Commands

```bash
# Build debug APK
buildozer -v android debug

# Build, deploy to device, and show logs
buildozer android debug deploy run logcat

# Clean build (if having issues)
buildozer android clean
buildozer -v android debug
```

The APK will be in the `bin/` folder.

## 🎨 Demo Screens

| Screen | Description |
|--------|-------------|
| **Home** | Navigation menu to all demos |
| **Animations** | Bounce, spin, and color animations |
| **Widgets** | Slider, switch, spinner, text input, progress bar |
| **Touch** | Touch detection with ripple effect |
| **Canvas** | Shape drawing with rotation |
| **About** | App information |

## 🔧 Customization

### Adding a New Screen

1. **Create the screen class** in `app_logic.py`:

```python
class MyNewScreen(BaseScreen):
    """Your new screen."""
    my_property = StringProperty("Hello")
    
    def my_method(self):
        self.my_property = "Updated!"
```

2. **Create a KV file** at `screens/myscreen.kv`:

```kv
<MyNewScreen>:
    name: 'myscreen'
    
    canvas.before:
        Color:
            rgba: 0.08, 0.08, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    BackButton:
        on_release: root.go_to_screen('home', 'right')
    
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        
        DemoTitle:
            text: "My New Screen"
        
        Label:
            text: root.my_property
        
        Button:
            text: "Click Me"
            on_release: root.my_method()
```

3. **Include the KV file** in `app_logic.kv`:

```kv
#:include screens/myscreen.kv
```

4. **Add to the screen manager** in `app_logic.kv`:

```kv
<DemoScreenManager>:
    ...
    MyNewScreen:
```

5. **Register for hot reload** in `main.py`:

```python
CLASSES = {
    ...
    "MyNewScreen": "app_logic",
}
```

6. **Add navigation** from home screen in `screens/home.kv`:

```kv
NavButton:
    text: "My New Screen"
    on_release: root.go_to_screen('myscreen', 'left')
```

### Adding Android Permissions

Edit `buildozer.spec`:

```spec
android.permissions = android.permission.INTERNET, android.permission.CAMERA
```

## 📝 Notes

- The `buildozer.spec` file is tracked in git (not ignored) to preserve build settings
- First Android build takes 15-30 minutes (downloads SDK/NDK)
- Subsequent builds are much faster
- Use `android.logcat_pid_only = True` to filter logs

## 📚 Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python-for-Android](https://python-for-android.readthedocs.io/)
- [Kaki Hot Reload](https://github.com/kivy/kaki)

## 📄 License

MIT License - Feel free to use this template for your projects!
