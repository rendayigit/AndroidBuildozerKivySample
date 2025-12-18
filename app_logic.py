from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty

# Note: We don't import Builder here anymore.
# Kaki loads the .kv file in main.py automatically.


class LiveLayout(BoxLayout):
    my_text_variable = StringProperty("Hello Kivy!")
    text_color = ListProperty([1, 1, 1, 1])

    def change_to_green(self):
        self.my_text_variable = "Green Button Clicked!"
        self.text_color = [0, 1, 0, 1]

    def change_to_pink(self):
        self.my_text_variable = "Pink Button Clicked!"
        self.text_color = [1, 0, 1, 1]


def build_layout():
    return LiveLayout()


# TEST BLOCK (For running this file directly without main.py)
if __name__ == "__main__":
    from kivy.app import App
    from kivy.lang import Builder

    class Test(App):
        def build(self):
            # We must load the KV manually ONLY if running this specific file directly
            Builder.load_file("app_logic.kv")
            return build_layout()

    Test().run()
