import os
from kivy.app import App
from kaki.app import App as KakiApp


class LiveApp(KakiApp, App):
    # 1. Tell Kaki the name of the class to load
    KV_FILES = []

    # 2. Tell Kaki where to find the 'logic' (class or module)
    CLASSES = {"LiveLayout": "app_logic"}

    # 3. Tell Kaki which folders to watch
    AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

    def build_app(self, first=False):
        try:
            # Import the file defined above
            import app_logic

            print("Reloading app_logic...")
            # Return the specific function from that file
            return app_logic.build_layout()
        except Exception as e:
            print(f"ERROR: {e}")
            from kivy.uix.label import Label

            return Label(text=str(e), color=(1, 0, 0, 1))


if __name__ == "__main__":
    LiveApp().run()
