import os
from kivy.app import App
from kivy.utils import platform


def _create_app_class():
    if platform == "android":
        from kivy.lang import Builder
        from app import AppScreenManager
        import screens as _screens  # noqa: F401

        class AndroidApp(App):
            def build(self):
                Builder.load_file("app/app.kv")
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
            KV_FILES = ["app/app.kv"]
            AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

            def build_app(self, first=False):  # type: ignore[override]
                import importlib
                import app
                import screens as screens_module

                importlib.reload(app)
                importlib.reload(screens_module)
                return app.AppScreenManager()

        return DesktopApp


if __name__ == "__main__":
    _create_app_class()().run()
