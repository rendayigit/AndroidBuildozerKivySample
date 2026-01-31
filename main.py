import os
import glob
import logging

# Suppress noisy debug logs from file watchers
logging.getLogger('watchdog').setLevel(logging.WARNING)
logging.getLogger('kivy').setLevel(logging.WARNING)

# Configure Kivy logging before importing other Kivy modules
from kivy.config import Config
Config.set('kivy', 'log_level', 'warning')

from kivy.app import App
from kivy.utils import platform


def _create_app_class():
    if platform == "android":
        from kivy.lang import Builder
        from app import AppScreenManager
        import screens as _screens  # noqa: F401

        class AndroidApp(App):
            def build(self):
                # Load all KV files - order matters: theme/components first, then screens, then app
                kv_files = [
                    "app/theme.kv",
                    "app/components.kv",
                    "screens/home.kv",
                    "screens/animation.kv",
                    "screens/widgets.kv",
                    "screens/touch.kv",
                    "screens/canvas.kv",
                    "screens/about.kv",
                    "app/app.kv",  # Load main app.kv last since it references the screens
                ]
                for kv_file in kv_files:
                    Builder.load_file(kv_file)
                return AppScreenManager()

        return AndroidApp
    else:
        from kaki.app import App as KakiApp

        class DesktopApp(KakiApp, App):
            CLASSES = {
                "AppScreenManager": "app",
                "BaseScreen": "app",
                "HomeScreen": "screens.home",
                "AnimationScreen": "screens.animation",
                "WidgetsScreen": "screens.widgets",
                "TouchScreen": "screens.touch",
                "CanvasScreen": "screens.canvas",
                "AboutScreen": "screens.about",
            }
            KV_FILES = [p.replace(os.getcwd() + os.sep, '') for p in glob.glob('**/*.kv', recursive=True)]
            AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

            def build_app(self, first=False):  # type: ignore[override]
                import importlib
                import app
                from screens import home, animation, widgets, touch, canvas, about

                # Save current screen before reload (self persists across rebuilds)
                if not first and hasattr(self, 'sm'):
                    self._current_screen = self.sm.current

                importlib.reload(app)
                importlib.reload(home)
                importlib.reload(animation)
                importlib.reload(widgets)
                importlib.reload(touch)
                importlib.reload(about)
                importlib.reload(canvas)

                self.sm = app.AppScreenManager()
                # Restore screen after reload
                if hasattr(self, '_current_screen'):
                    self.sm.current = self._current_screen
                return self.sm

        return DesktopApp


if __name__ == "__main__":
    _create_app_class()().run()
