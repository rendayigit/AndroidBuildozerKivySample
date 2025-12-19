"""
Kivy Demo Application - Showcasing Various Kivy Features
This module contains all the UI logic and components for the demo app.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.logger import Logger
import random


class DemoScreenManager(ScreenManager):
    """Main screen manager for navigating between demo screens."""
    pass


class BaseScreen(Screen):
    """Base screen class with navigation helper."""
    
    def go_to_screen(self, screen_name, direction='left'):
        """Navigate to a screen with transition direction."""
        sm = self.manager
        if sm:
            sm.transition.direction = direction
            sm.current = screen_name


class HomeScreen(BaseScreen):
    """Home screen with navigation to different demo sections."""
    pass


class AnimationDemo(BaseScreen):
    """Demo screen showcasing various animations."""
    
    box_x = NumericProperty(0.1)
    box_y = NumericProperty(0.5)
    box_color = ListProperty([1, 0.3, 0.3, 1])
    rotation_angle = NumericProperty(0)
    scale_factor = NumericProperty(1)
    
    def on_enter(self):
        """Start idle animation when entering screen."""
        self.start_idle_animation()
    
    def on_leave(self):
        """Stop animations when leaving screen."""
        Animation.cancel_all(self)
    
    def start_idle_animation(self):
        """Subtle pulsing animation."""
        anim = Animation(scale_factor=1.1, duration=0.8) + Animation(scale_factor=1, duration=0.8)
        anim.repeat = True
        anim.start(self)
    
    def animate_bounce(self):
        """Bouncing animation demo."""
        Animation.cancel_all(self)
        anim = (
            Animation(box_x=0.8, box_y=0.7, duration=0.3, t='out_quad') +
            Animation(box_x=0.2, box_y=0.3, duration=0.3, t='out_bounce') +
            Animation(box_x=0.5, box_y=0.5, duration=0.2, t='out_elastic')
        )
        anim.bind(on_complete=lambda *args: self.start_idle_animation())
        anim.start(self)
    
    def animate_spin(self):
        """Spinning animation demo."""
        anim = Animation(rotation_angle=self.rotation_angle + 360, duration=0.8, t='out_cubic')
        anim.start(self)
    
    def animate_color_cycle(self):
        """Color cycling animation."""
        colors = [
            [1, 0.3, 0.3, 1],  # Red
            [0.3, 1, 0.3, 1],  # Green
            [0.3, 0.3, 1, 1],  # Blue
            [1, 1, 0.3, 1],    # Yellow
            [1, 0.3, 1, 1],    # Magenta
            [0.3, 1, 1, 1],    # Cyan
        ]
        anim = Animation(duration=0)
        for color in colors:
            anim += Animation(box_color=color, duration=0.3)
        anim.start(self)
    
    def animate_all(self):
        """Combined animation showcase."""
        self.animate_bounce()
        self.animate_spin()
        self.animate_color_cycle()


class WidgetDemo(BaseScreen):
    """Demo screen showcasing various Kivy widgets."""
    
    slider_value = NumericProperty(50)
    progress_value = NumericProperty(0)
    switch_state = BooleanProperty(False)
    spinner_text = StringProperty("Select Option")
    text_input_value = StringProperty("")
    status_text = StringProperty("Interact with widgets above")
    
    def on_enter(self):
        """Start progress animation when entering."""
        self.animate_progress()
    
    def on_leave(self):
        """Stop progress animation when leaving."""
        Animation.cancel_all(self)
    
    def animate_progress(self):
        """Animate progress bar."""
        self.progress_value = 0
        anim = Animation(progress_value=100, duration=3)
        anim.bind(on_complete=lambda *args: Clock.schedule_once(lambda dt: self.animate_progress(), 1))
        anim.start(self)
    
    def on_slider_change(self, value):
        """Handle slider value change."""
        self.slider_value = value
        self.status_text = f"Slider: {value:.0f}%"
        Logger.info(f'WidgetDemo: Slider value changed to {value:.1f}')
    
    def on_switch_change(self, active):
        """Handle switch state change."""
        self.switch_state = active
        self.status_text = f"Switch: {'ON' if active else 'OFF'}"
        Logger.info(f'WidgetDemo: Switch is now {"ON" if active else "OFF"}')
    
    def on_spinner_select(self, text):
        """Handle spinner selection."""
        self.spinner_text = text
        self.status_text = f"Selected: {text}"
        Logger.info(f'WidgetDemo: Selected {text}')
    
    def on_text_change(self, text):
        """Handle text input change."""
        self.text_input_value = text
        if text:
            self.status_text = f"Typed: {text[:20]}..."
    
    def on_checkbox_change(self, active):
        """Handle checkbox change."""
        self.status_text = f"Checkbox: {'Checked' if active else 'Unchecked'}"


class TouchDemo(BaseScreen):
    """Demo screen for touch/gesture interactions."""
    
    touch_x = NumericProperty(200)
    touch_y = NumericProperty(300)
    touch_info = StringProperty("Touch the area below!")
    ripple_opacity = NumericProperty(0)
    ripple_size = NumericProperty(0)
    touch_count = NumericProperty(0)
    
    def handle_touch(self, touch_pos, widget):
        """Handle touch events in the demo area."""
        self.touch_x = touch_pos[0]
        self.touch_y = touch_pos[1]
        self.touch_count += 1
        self.touch_info = f"Touch #{self.touch_count}: ({touch_pos[0]:.0f}, {touch_pos[1]:.0f})"
        
        # Trigger ripple animation
        self.ripple_opacity = 0.6
        self.ripple_size = 20
        anim = Animation(ripple_size=150, ripple_opacity=0, duration=0.4, t='out_quad')
        anim.start(self)
        
        Logger.info(f'TouchDemo: Touch at {touch_pos}')
    
    def reset_touches(self):
        """Reset touch counter."""
        self.touch_count = 0
        self.touch_info = "Touch counter reset!"


class CanvasDemo(BaseScreen):
    """Demo screen showcasing canvas drawing."""
    
    shape_color = ListProperty([0.2, 0.6, 1, 1])
    shape_rotation = NumericProperty(0)
    
    def randomize_color(self):
        """Randomize shape color."""
        self.shape_color = [random.random(), random.random(), random.random(), 1]
    
    def rotate_shape(self):
        """Animate shape rotation."""
        anim = Animation(shape_rotation=self.shape_rotation + 45, duration=0.3, t='out_back')
        anim.start(self)


class AboutScreen(BaseScreen):
    """About screen with app information."""
    
    version_text = StringProperty("Version 1.0.0")
    info_text = StringProperty(
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


# Legacy support - keeping original for reference
class LiveLayout(BoxLayout):
    """Original simple layout - kept for backwards compatibility."""
    my_text_variable = StringProperty("Hello Kivy!")
    text_color = ListProperty([1, 1, 1, 1])

    def change_to_green(self):
        Logger.info('MyApp: Green button was pressed!')
        self.my_text_variable = "Green Button Clicked!"
        self.text_color = [0, 1, 0, 1]

    def change_to_pink(self):
        self.my_text_variable = "Pink Button Clicked!"
        self.text_color = [1, 0, 1, 1]


def build_layout():
    """Build and return the main application layout."""
    return DemoScreenManager()


# TEST BLOCK (For running this file directly without main.py)
if __name__ == "__main__":
    from kivy.app import App
    from kivy.lang import Builder

    class Test(App):
        def build(self):
            Builder.load_file("app_logic.kv")
            return build_layout()

    Test().run()
