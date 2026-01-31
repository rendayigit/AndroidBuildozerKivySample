from kivy.uix.screenmanager import ScreenManager, Screen


class AppScreenManager(ScreenManager):
    pass


class BaseScreen(Screen):
    def on_enter(self):
        print(f"[KivyDemo] Opened screen: {self.name}")

    def go_to(self, screen_name, direction="left"):
        if self.manager:
            self.manager.transition.direction = direction
            self.manager.current = screen_name
