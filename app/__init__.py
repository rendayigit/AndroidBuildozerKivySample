from kivy.app import App
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen


THEMES = {
    "midnight": {
        "label": "Midnight",
        "bg_color": [0.06, 0.065, 0.09, 1],
        "glow_color": [0.35, 0.55, 1.0, 0.16],
        "surface_color": [0.10, 0.11, 0.14, 1],
        "surface_alt_color": [0.14, 0.15, 0.19, 1],
        "border_color": [0.18, 0.19, 0.24, 1],
        "primary_color": [0.35, 0.55, 1.0, 1],
        "accent_color": [0.55, 0.85, 0.65, 1],
        "danger_color": [0.85, 0.35, 0.40, 1],
        "text_primary_color": [0.95, 0.96, 0.98, 1],
        "text_secondary_color": [0.75, 0.77, 0.82, 1],
        "text_muted_color": [0.50, 0.53, 0.60, 1],
    },
    "sunset": {
        "label": "Sunset",
        "bg_color": [0.12, 0.08, 0.11, 1],
        "glow_color": [1.0, 0.50, 0.32, 0.14],
        "surface_color": [0.17, 0.12, 0.16, 1],
        "surface_alt_color": [0.23, 0.16, 0.20, 1],
        "border_color": [0.34, 0.22, 0.24, 1],
        "primary_color": [1.0, 0.53, 0.32, 1],
        "accent_color": [0.98, 0.78, 0.38, 1],
        "danger_color": [0.87, 0.30, 0.34, 1],
        "text_primary_color": [0.99, 0.95, 0.93, 1],
        "text_secondary_color": [0.90, 0.82, 0.79, 1],
        "text_muted_color": [0.72, 0.62, 0.60, 1],
    },
}


class AppScreenManager(ScreenManager):
    theme_name = StringProperty("midnight")
    theme_label = StringProperty(THEMES["midnight"]["label"])
    status_message = StringProperty("Explore the sample screens to see Kivy patterns in action.")
    status_source = StringProperty("home")
    selected_demo = StringProperty("Widgets")
    callback_count = NumericProperty(0)

    bg_color = ListProperty(THEMES["midnight"]["bg_color"])
    glow_color = ListProperty(THEMES["midnight"]["glow_color"])
    surface_color = ListProperty(THEMES["midnight"]["surface_color"])
    surface_alt_color = ListProperty(THEMES["midnight"]["surface_alt_color"])
    border_color = ListProperty(THEMES["midnight"]["border_color"])
    primary_color = ListProperty(THEMES["midnight"]["primary_color"])
    accent_color = ListProperty(THEMES["midnight"]["accent_color"])
    danger_color = ListProperty(THEMES["midnight"]["danger_color"])
    text_primary_color = ListProperty(THEMES["midnight"]["text_primary_color"])
    text_secondary_color = ListProperty(THEMES["midnight"]["text_secondary_color"])
    text_muted_color = ListProperty(THEMES["midnight"]["text_muted_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_theme(self.theme_name)

    def sync_app_state(self):
        running_app = App.get_running_app()
        if not running_app:
            return

        keys = (
            "theme_name",
            "theme_label",
            "status_message",
            "status_source",
            "selected_demo",
            "callback_count",
            "bg_color",
            "glow_color",
            "surface_color",
            "surface_alt_color",
            "border_color",
            "primary_color",
            "accent_color",
            "danger_color",
            "text_primary_color",
            "text_secondary_color",
            "text_muted_color",
        )
        for key in keys:
            if hasattr(running_app, key):
                setattr(running_app, key, getattr(self, key))

    def set_selected_demo(self, selected_demo):
        self.selected_demo = selected_demo
        self.sync_app_state()

    def apply_theme(self, theme_name):
        palette = THEMES.get(theme_name, THEMES["midnight"])
        self.theme_name = theme_name if theme_name in THEMES else "midnight"
        self.theme_label = palette["label"]
        self.bg_color = palette["bg_color"]
        self.glow_color = palette["glow_color"]
        self.surface_color = palette["surface_color"]
        self.surface_alt_color = palette["surface_alt_color"]
        self.border_color = palette["border_color"]
        self.primary_color = palette["primary_color"]
        self.accent_color = palette["accent_color"]
        self.danger_color = palette["danger_color"]
        self.text_primary_color = palette["text_primary_color"]
        self.text_secondary_color = palette["text_secondary_color"]
        self.text_muted_color = palette["text_muted_color"]
        self.sync_app_state()

    def cycle_theme(self):
        theme_names = list(THEMES)
        next_index = (theme_names.index(self.theme_name) + 1) % len(theme_names)
        next_theme = theme_names[next_index]
        self.apply_theme(next_theme)
        self.record_event("theme", f"Theme changed to {self.theme_label}", selected_demo="Theme")

    def record_event(self, source, message, selected_demo=None):
        self.callback_count += 1
        self.status_source = source
        self.status_message = message
        if selected_demo:
            self.selected_demo = selected_demo
        self.sync_app_state()


class BaseScreen(Screen):
    def on_enter(self, *args):
        print(f"[KivyDemo] Opened screen: {self.name}")

    def go_to(self, screen_name, direction="left"):
        if self.manager:
            self.manager.transition.direction = direction
            self.manager.current = screen_name

    def record_event(self, message, selected_demo=None):
        if self.manager and hasattr(self.manager, "record_event"):
            self.manager.record_event(self.name, message, selected_demo=selected_demo)

    def cycle_theme(self):
        if self.manager and hasattr(self.manager, "cycle_theme"):
            self.manager.cycle_theme()
