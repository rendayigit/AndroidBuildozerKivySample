import os
import glob
import logging
import importlib
import pkgutil

# Suppress noisy debug logs from file watchers
logging.getLogger('watchdog').setLevel(logging.WARNING)
logging.getLogger('kivy').setLevel(logging.WARNING)

# Configure Kivy logging before importing other Kivy modules
from kivy.config import Config
Config.set('kivy', 'log_level', 'warning')

from kivy.app import App
from kivy.utils import platform


def _discover_screen_modules():
    """Discover all screen modules in the screens package."""
    import screens
    modules = {}
    for importer, modname, ispkg in pkgutil.iter_modules(screens.__path__):
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

        class AndroidApp(App):
            def build(self):
                for kv_file in _get_kv_files_ordered():
                    Builder.load_file(kv_file)
                return AppScreenManager()

        return AndroidApp
    else:
        from kaki.app import App as KakiApp

        class DesktopApp(KakiApp, App):
            CLASSES = _discover_screen_classes(_discover_screen_modules())
            KV_FILES = [p.replace(os.getcwd() + os.sep, '') for p in glob.glob('**/*.kv', recursive=True)]
            AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

            def build_app(self, first=False):  # type: ignore[override]
                import app

                # Save current screen before reload (self persists across rebuilds)
                if not first and hasattr(self, 'sm'):
                    self._current_screen = self.sm.current

                # Reload all screen modules dynamically
                screen_modules = _discover_screen_modules()
                importlib.reload(app)
                for module in screen_modules.values():
                    importlib.reload(module)

                self.sm = app.AppScreenManager()
                # Restore screen after reload
                if hasattr(self, '_current_screen'):
                    self.sm.current = self._current_screen
                return self.sm

        return DesktopApp


if __name__ == "__main__":
    _create_app_class()().run()
