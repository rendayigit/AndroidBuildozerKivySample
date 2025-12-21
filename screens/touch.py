from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty

from app import BaseScreen


class TouchScreen(BaseScreen):
    touch_x = NumericProperty(200)
    touch_y = NumericProperty(300)
    touch_info = StringProperty("Touch the area below!")
    ripple_opacity = NumericProperty(0)
    ripple_size = NumericProperty(0)
    touch_count = NumericProperty(0)

    def handle_touch(self, pos, _widget):
        self.touch_x, self.touch_y = pos
        self.touch_count += 1
        self.touch_info = f"Touch #{self.touch_count}: ({pos[0]:.0f}, {pos[1]:.0f})"

        self.ripple_opacity = 0.6
        self.ripple_size = 20
        anim = Animation(ripple_size=150, ripple_opacity=0, duration=0.4, t="out_quad")
        anim.start(self)

    def reset_touches(self):
        self.touch_count = 0
        self.touch_info = "Touch counter reset!"
