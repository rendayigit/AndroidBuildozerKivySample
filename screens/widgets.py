from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from app import BaseScreen


class WidgetsScreen(BaseScreen):
    slider_value = NumericProperty(50)
    progress_value = NumericProperty(0)
    switch_state = BooleanProperty(False)
    spinner_text = StringProperty("Select Option")
    status_text = StringProperty("Interact with widgets above")

    def on_enter(self, *args):
        super().on_enter(*args)
        self._animate_progress()

    def on_leave(self, *args):
        super().on_leave(*args)
        Animation.cancel_all(self)

    def _animate_progress(self):
        self.progress_value = 0
        anim = Animation(progress_value=100, duration=3)
        anim.bind(on_complete=lambda *_: Clock.schedule_once(lambda _: self._animate_progress(), 1))
        anim.start(self)

    def on_slider_change(self, value):
        self.slider_value = value
        self.status_text = f"Slider: {value:.0f}%"

    def on_switch_change(self, active):
        self.switch_state = active
        self.status_text = f"Switch: {'ON' if active else 'OFF'}"

    def on_spinner_select(self, text):
        self.spinner_text = text
        self.status_text = f"Selected: {text}"

    def on_text_change(self, text):
        if text:
            self.status_text = f"Typed: {text[:20]}..."

    def on_checkbox_change(self, active):
        self.status_text = f"Checkbox: {'Checked' if active else 'Unchecked'}"
