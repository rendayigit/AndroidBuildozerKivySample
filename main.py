import os
from kivy.app import App
from kivy.utils import platform

# ---------------------------------------------------------
# SCENARIO 1: ON ANDROID (Standard Run)
# ---------------------------------------------------------
if platform == "android":
    import app_logic
    from kivy.lang import Builder

    class LiveApp(App):
        def build(self):
            # Manually load the KV file since it doesn't match the App name
            Builder.load_file("app_logic.kv")
            return app_logic.build_layout()


# ---------------------------------------------------------
# SCENARIO 2: ON PC (Hot Reload enabled)
# ---------------------------------------------------------
else:
    from kaki.app import App as KakiApp

    class LiveApp(KakiApp, App):
        # Kaki loads these files automatically on PC for hot reload
        KV_FILES = ["app_logic.kv"]
        
        # Register all classes that should be hot-reloadable
        CLASSES = {
            "DemoScreenManager": "app_logic",
            "BaseScreen": "app_logic",
            "HomeScreen": "app_logic",
            "AnimationDemo": "app_logic",
            "WidgetDemo": "app_logic",
            "TouchDemo": "app_logic",
            "CanvasDemo": "app_logic",
            "AboutScreen": "app_logic",
            "LiveLayout": "app_logic",  # Legacy support
        }
        
        # Watch all KV files for hot reload
        # Note: Only list the main KV file - it includes the others via #:include
        KV_FILES = [
            "app_logic.kv",
        ]
        
        AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

        def build_app(self, first=False):
            try:
                import app_logic
                import importlib

                importlib.reload(app_logic)
                print("Reloading app_logic...")
                return app_logic.build_layout()
            except Exception as e:
                print(f"ERROR: {e}")
                from kivy.uix.label import Label
                return Label(text=str(e), color=(1, 0, 0, 1))


if __name__ == "__main__":
    LiveApp().run()
