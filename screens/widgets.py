from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from app import BaseScreen


class WidgetsScreen(BaseScreen):
    slider_value = NumericProperty(50)
    progress_value = NumericProperty(0)
    switch_state = BooleanProperty(False)
    checkbox_state = BooleanProperty(False)
    spinner_text = StringProperty("Select Option")
    text_value = StringProperty("")
    radio_choice = StringProperty("Kivy")
    status_text = StringProperty("Interact with widgets above")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._progress_event = None

    def on_enter(self, *args):
        super().on_enter(*args)
        self.record_event("Opened interactive widgets and form controls.", selected_demo="Widgets")
        self._animate_progress()

    def on_leave(self, *args):
        super().on_leave(*args)
        Animation.cancel_all(self)
        if self._progress_event is not None:
            self._progress_event.cancel()
            self._progress_event = None

    def _animate_progress(self, *_):
        if self._progress_event is not None:
            self._progress_event.cancel()
            self._progress_event = None
        self.progress_value = 0
        anim = Animation(progress_value=100, duration=3.2)
        anim.bind(on_complete=self._queue_progress_restart)
        anim.start(self)

    def _queue_progress_restart(self, *_):
        self._progress_event = Clock.schedule_once(self._animate_progress, 1.0)

    def on_slider_change(self, value):
        self.slider_value = value
        self.status_text = f"Slider moved to {value:.0f}%"

    def sync_progress(self):
        Animation.cancel_all(self)
        if self._progress_event is not None:
            self._progress_event.cancel()
            self._progress_event = None
        self.progress_value = self.slider_value
        self.status_text = f"Progress synced to {self.progress_value:.0f}%"
        self.record_event(self.status_text, selected_demo="ProgressBar")

    def on_switch_change(self, active):
        self.switch_state = active
        self.status_text = f"Switch is {'ON' if active else 'OFF'}"
        self.record_event(self.status_text, selected_demo="Switches")

    def on_spinner_select(self, text):
        if text == "Select Option":
            return
        self.spinner_text = text
        self.status_text = f"Spinner selected {text}"
        self.record_event(self.status_text, selected_demo="Spinner")

    def on_text_change(self, text):
        self.text_value = text
        if text:
            self.status_text = f"Typed: {text[:24]}"
        else:
            self.status_text = "Waiting for text input"

    def on_checkbox_change(self, active):
        self.checkbox_state = active
        self.status_text = f"Checkbox {'checked' if active else 'cleared'}"

    def on_radio_select(self, choice):
        self.radio_choice = choice
        self.status_text = f"Radio picked {choice}"
        self.record_event(self.status_text, selected_demo="Radio Buttons")

    def send_status_home(self):
        self.record_event(self.status_text, selected_demo="Callbacks")
        self.go_to("home", "right")
