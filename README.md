# Kivy Android App Template

A boilerplate for building Android apps with Python, Kivy, and Buildozer. Includes hot reload for desktop development.

## Setup

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev xclip
```

### Python Environment

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

### Desktop (VS Code)

Use the **Run App** or **Run Hot Reload** tasks.

### Desktop (Terminal)

```bash
.venv/bin/python main.py -m screen:phone_oneplus_6t,portrait,scale=0.3
```

### Build Android APK

```bash
buildozer -v android debug
```

## License

MIT
