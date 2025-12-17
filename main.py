import os
from kivy.app import App
from kivy.utils import platform

# ---------------------------------------------------------
# SCENARIO 1: ON ANDROID (Standard Run, No Kaki)
# ---------------------------------------------------------
if platform == "android":
    import app_logic

    class LiveApp(App):
        def build(self):
            return app_logic.build_layout()


# ---------------------------------------------------------
# SCENARIO 2: ON PC (Hot Reload enabled)
# ---------------------------------------------------------
else:
    from kaki.app import App as KakiApp

    class LiveApp(KakiApp, App):
        KV_FILES = []
        CLASSES = {"LiveLayout": "app_logic"}
        AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

        def build_app(self, first=False):
            try:
                import app_logic

                # Force reload the module so changes appear
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
