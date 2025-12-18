import os
from kivy.app import App
from kivy.utils import platform

# ---------------------------------------------------------
# SCENARIO 1: ON ANDROID (Standard Run)
# ---------------------------------------------------------
if platform == "android":
    import app_logic
    from kivy.lang import Builder  # <--- ADD THIS

    class LiveApp(App):
        def build(self):
            # <--- ADD THIS LINE
            # Manually load the KV file since it doesn't match the App name
            Builder.load_file("app_logic.kv")

            return app_logic.build_layout()


# ---------------------------------------------------------
# SCENARIO 2: ON PC (Hot Reload enabled)
# ---------------------------------------------------------
else:
    from kaki.app import App as KakiApp

    class LiveApp(KakiApp, App):
        # Kaki loads this automatically on PC
        KV_FILES = ["app_logic.kv"]
        CLASSES = {"LiveLayout": "app_logic"}
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
