from typing import Any

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from app import BaseScreen


class ComponentsScreen(BaseScreen):
    active_tab = StringProperty("buttons")
    button_style = StringProperty("Primary")
    selected_layout = StringProperty("BoxLayout")
    action_summary = StringProperty(
        "Use the tabs below to explore buttons, layouts, popups, images, and shared callbacks."
    )
    popup_count = NumericProperty(0)
    theme_preview = StringProperty("Midnight")

    def on_enter(self, *args):
        super().on_enter(*args)
        if self.manager:
            self.theme_preview = self.manager.theme_label
        self.record_event("Opened components, layouts, and popup samples.", selected_demo="Components")

    def select_tab(self, tab_name):
        if self.active_tab == tab_name:
            return
        self.active_tab = tab_name
        summaries = {
            "buttons": "Rounded and outlined buttons can live alongside image and label content.",
            "layouts": "Layouts decide how widgets share space, and Splitter lets users resize a panel.",
            "feedback": "Theme changes and callbacks can travel back to the home dashboard.",
        }
        self.action_summary = summaries.get(tab_name, self.action_summary)
        self.record_event(self.action_summary, selected_demo="Tabs")

    def choose_button_style(self, style_name):
        self.button_style = style_name
        self.action_summary = f"{style_name} style selected for rounded buttons."
        self.record_event(self.action_summary, selected_demo="Buttons")

    def choose_layout(self, layout_name):
        self.selected_layout = layout_name
        self.action_summary = f"{layout_name} arranges widgets with a different strategy."
        self.record_event(self.action_summary, selected_demo="Layouts")

    def cycle_theme_demo(self):
        self.cycle_theme()
        if self.manager:
            self.theme_preview = self.manager.theme_label
        self.action_summary = f"Theme switched to {self.theme_preview}."

    def show_sample_popup(self):
        primary_color = self.manager.primary_color if self.manager else [0.35, 0.55, 1.0, 1]
        surface_color = self.manager.surface_alt_color if self.manager else [0.14, 0.15, 0.19, 1]
        text_color = self.manager.text_primary_color if self.manager else [0.95, 0.96, 0.98, 1]

        popup = Popup(
            title="Popup Sample",
            title_align="center",
            separator_color=primary_color,
            size_hint=(0.86, None),
            height=260,
            auto_dismiss=False,
        )

        content = BoxLayout(orientation="vertical", padding=18, spacing=14)
        content.add_widget(
            Label(
                text=(
                    "Popups are useful for focused flows such as confirmation,\n"
                    "secondary actions, or compact form steps."
                ),
                halign="center",
                valign="middle",
                color=text_color,
            )
        )

        actions = BoxLayout(size_hint_y=None, height=46, spacing=10)
        confirm: Any = Button(
            text="Send Callback",
            background_normal="",
            background_color=primary_color,
            color=text_color,
        )
        dismiss: Any = Button(
            text="Close",
            background_normal="",
            background_color=surface_color,
            color=text_color,
        )
        getattr(confirm, "bind")(on_release=lambda *_: self._confirm_popup(popup))
        getattr(dismiss, "bind")(on_release=lambda *_: self._dismiss_popup(popup))
        actions.add_widget(confirm)
        actions.add_widget(dismiss)

        content.add_widget(actions)
        popup.content = content
        popup.open()

    def _confirm_popup(self, popup):
        self.popup_count += 1
        self.action_summary = f"Popup confirmed {self.popup_count} time(s)."
        self.record_event("Popup confirmed and callback sent back to home.", selected_demo="Popups")
        popup.dismiss()

    def _dismiss_popup(self, popup):
        self.action_summary = "Popup dismissed without sending a callback."
        popup.dismiss()

    def send_callback_home(self):
        self.record_event(
            f"Components screen sent {self.selected_layout} guidance back to home.",
            selected_demo="Callbacks",
        )
        self.go_to("home", "right")