from kivy.properties import StringProperty

from app import BaseScreen


class AboutScreen(BaseScreen):
    version = StringProperty("Version 1.0.0")
    description = StringProperty(
        "Kivy Demo Application\n\n"
        "A template project for developing\n"
        "Android apps with Python.\n\n"
        "Features:\n"
        "• Screen Navigation\n"
        "• Animations\n"
        "• Widget Showcase\n"
        "• Touch Handling\n"
        "• Canvas Drawing\n"
        "• Hot Reload (Desktop)"
    )
