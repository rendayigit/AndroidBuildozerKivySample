from kivy.properties import StringProperty

from app import BaseScreen


class AboutScreen(BaseScreen):
    version = StringProperty("Version 1.2.0")
    description = StringProperty(
        "Kivy Demo Application\n\n"
        "A broader sample project for developing\n"
        "Android apps with Python and Kivy.\n\n"
        "Features:\n"
        "• Screen Navigation\n"
        "• Shared Theme State\n"
        "• Tabs, Popups, Splitter\n"
        "• Animations\n"
        "• Widget Showcase + Forms\n"
        "• Touch Handling\n"
        "• Canvas Drawing\n"
        "• Callbacks Across Screens\n"
        "• Hot Reload (Desktop)"
    )
