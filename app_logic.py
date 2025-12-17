from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

# 1. DEFINE THE UI (The "KV" Language)
# This looks like CSS/HTML. We define the look here.
KV_CODE = """
<LiveLayout>:
    orientation: 'vertical'
    padding: 50
    spacing: 20
    
    # Set a background color (Canvas instructions)
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1  # Dark Grey
        Rectangle:
            pos: self.pos
            size: self.size

    # THE LABEL
    Label:
        text: root.my_text_variable   # Bind to the property defined in Python
        font_size: '40sp'
        color: root.text_color
        bold: True

    # BUTTON 1
    Button:
        text: "Make it Green"
        background_color: 0, 1, 0, 1
        size_hint_y: None             # Don't stretch vertically
        height: '60dp'                # Fixed height
        on_press: root.change_to_green()

    # BUTTON 2
    Button:
        text: "Make it Pink"
        background_color: 1, 0, 1, 1
        size_hint_y: None
        height: '60dp'
        on_press: root.change_to_pink()
"""


# 2. DEFINE THE LOGIC
class LiveLayout(BoxLayout):
    # These are "Reactive" properties.
    # If you change 'my_text_variable' in code, the Label updates automatically!
    my_text_variable = StringProperty("Hello Kivy!")
    text_color = ListProperty([1, 1, 1, 1])  # White (R, G, B, A)

    def change_to_green(self):
        self.my_text_variable = "Green Button Clicked!"
        self.text_color = [0, 1, 0, 1]  # Green

    def change_to_pink(self):
        self.my_text_variable = "Pink Button Clicked!"
        self.text_color = [1, 0, 1, 1]  # Pink


# 3. BUILD FUNCTION (Called by main.py)
def build_layout():
    # Clear any existing cache to ensure Hot Reload works perfectly
    Builder.unload_file(__file__)
    Builder.load_string(KV_CODE)
    return LiveLayout()


# 4. TEST BLOCK (Allows running this file directly)
if __name__ == "__main__":
    from kivy.app import App

    class Test(App):
        def build(self):
            return build_layout()

    Test().run()
