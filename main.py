import os
import glob
import logging
import importlib
import pkgutil
from typing import Any, Optional

# Suppress noisy debug logs from file watchers
logging.getLogger('watchdog').setLevel(logging.WARNING)
logging.getLogger('kivy').setLevel(logging.WARNING)

# Configure Kivy logging before importing other Kivy modules
from kivy.config import Config
Config.set('kivy', 'log_level', 'warning')

from kivy.app import App
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.utils import platform


APP_STATE_DEFAULTS = {
    "theme_name": "midnight",
    "theme_label": "Midnight",
    "status_message": "Explore the sample screens to see Kivy patterns in action.",
    "status_source": "home",
    "selected_demo": "Widgets",
    "callback_count": 0,
    "bg_color": [0.06, 0.065, 0.09, 1],
    "glow_color": [0.35, 0.55, 1.0, 0.16],
    "surface_color": [0.10, 0.11, 0.14, 1],
    "surface_alt_color": [0.14, 0.15, 0.19, 1],
    "border_color": [0.18, 0.19, 0.24, 1],
    "primary_color": [0.35, 0.55, 1.0, 1],
    "accent_color": [0.55, 0.85, 0.65, 1],
    "danger_color": [0.85, 0.35, 0.40, 1],
    "text_primary_color": [0.95, 0.96, 0.98, 1],
    "text_secondary_color": [0.75, 0.77, 0.82, 1],
    "text_muted_color": [0.50, 0.53, 0.60, 1],
}


class SharedAppStateMixin:
    theme_name = StringProperty(APP_STATE_DEFAULTS["theme_name"])
    theme_label = StringProperty(APP_STATE_DEFAULTS["theme_label"])
    status_message = StringProperty(APP_STATE_DEFAULTS["status_message"])
    status_source = StringProperty(APP_STATE_DEFAULTS["status_source"])
    selected_demo = StringProperty(APP_STATE_DEFAULTS["selected_demo"])
    callback_count = NumericProperty(APP_STATE_DEFAULTS["callback_count"])

    bg_color = ListProperty(APP_STATE_DEFAULTS["bg_color"])
    glow_color = ListProperty(APP_STATE_DEFAULTS["glow_color"])
    surface_color = ListProperty(APP_STATE_DEFAULTS["surface_color"])
    surface_alt_color = ListProperty(APP_STATE_DEFAULTS["surface_alt_color"])
    border_color = ListProperty(APP_STATE_DEFAULTS["border_color"])
    primary_color = ListProperty(APP_STATE_DEFAULTS["primary_color"])
    accent_color = ListProperty(APP_STATE_DEFAULTS["accent_color"])
    danger_color = ListProperty(APP_STATE_DEFAULTS["danger_color"])
    text_primary_color = ListProperty(APP_STATE_DEFAULTS["text_primary_color"])
    text_secondary_color = ListProperty(APP_STATE_DEFAULTS["text_secondary_color"])
    text_muted_color = ListProperty(APP_STATE_DEFAULTS["text_muted_color"])


def _discover_screen_modules():
    """Discover all screen modules in the screens package."""
    import screens
    modules = {}
    for _importer, modname, ispkg in pkgutil.iter_modules(screens.__path__):
        if not ispkg and not modname.startswith('_'):
            modules[modname] = importlib.import_module(f'screens.{modname}')
    return modules


def _discover_screen_classes(modules):
    """Build CLASSES dict by finding Screen subclasses in modules."""
    from kivy.uix.screenmanager import Screen
    classes = {
        "AppScreenManager": "app",
        "BaseScreen": "app",
    }
    for modname, module in modules.items():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, Screen) and 
                attr is not Screen and
                attr_name.endswith('Screen')):
                classes[attr_name] = f"screens.{modname}"
    return classes


def _get_kv_files_ordered():
    """Get KV files in correct load order: theme/components, screens, then app.kv last."""
    kv_files = []
    # Load theme and components first
    for kv in ['app/theme.kv', 'app/components.kv']:
        if os.path.exists(kv):
            kv_files.append(kv)
    # Load screen KV files
    kv_files.extend(sorted(glob.glob('screens/*.kv')))
    # Load app.kv last (it references the screens)
    if os.path.exists('app/app.kv'):
        kv_files.append('app/app.kv')
    return kv_files


def _create_app_class():
    if platform == "android":
        from kivy.lang import Builder
        from app import AppScreenManager
        import screens as _screens  # noqa: F401 - triggers screen imports

        class AndroidApp(SharedAppStateMixin, App):
            def build(self):
                for kv_file in _get_kv_files_ordered():
                    Builder.load_file(kv_file)
                return AppScreenManager()

        return AndroidApp
    else:
        from kaki.app import App as KakiApp

        class DesktopApp(KakiApp, SharedAppStateMixin, App):
            CLASSES = _discover_screen_classes(_discover_screen_modules())
            KV_FILES = [p.replace(os.getcwd() + os.sep, '') for p in glob.glob('**/*.kv', recursive=True)]
            AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]
            sm: Optional[Any] = None
            _current_screen = ""

            def build_app(self, first=False):  # type: ignore[override]
                import app

                # Save current screen before reload (self persists across rebuilds)
                if not first and self.sm is not None:
                    self._current_screen = self.sm.current

                # Reload all screen modules dynamically
                screen_modules = _discover_screen_modules()
                importlib.reload(app)
                for module in screen_modules.values():
                    importlib.reload(module)

                self.sm = app.AppScreenManager()
                # Restore screen after reload
                if self._current_screen:
                    self.sm.current = self._current_screen
                return self.sm

        return DesktopApp


if __name__ == "__main__":
    _create_app_class()().run()
