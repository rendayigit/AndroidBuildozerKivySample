from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty

from app import BaseScreen


class AnimationScreen(BaseScreen):
    box_x = NumericProperty(0.1)
    box_y = NumericProperty(0.5)
    box_color = ListProperty([1, 0.3, 0.3, 1])
    rotation_angle = NumericProperty(0)
    scale_factor = NumericProperty(1)

    def on_enter(self, *args):
        super().on_enter(*args)
        self._start_idle()

    def on_leave(self, *args):
        super().on_leave(*args)
        Animation.cancel_all(self)

    def _start_idle(self):
        anim = Animation(scale_factor=1.1, duration=0.8)
        anim += Animation(scale_factor=1, duration=0.8)
        anim.repeat = True
        anim.start(self)

    def bounce(self):
        Animation.cancel_all(self)
        anim = (
            Animation(box_x=0.8, box_y=0.7, duration=0.3, t="out_quad")
            + Animation(box_x=0.2, box_y=0.3, duration=0.3, t="out_bounce")
            + Animation(box_x=0.5, box_y=0.5, duration=0.2, t="out_elastic")
        )
        anim.bind(on_complete=lambda *_: self._start_idle())
        anim.start(self)

    def spin(self):
        anim = Animation(rotation_angle=self.rotation_angle + 360, duration=0.8, t="out_cubic")
        anim.start(self)

    def cycle_colors(self):
        colors = [
            [1, 0.3, 0.3, 1],
            [0.3, 1, 0.3, 1],
            [0.3, 0.3, 1, 1],
            [1, 1, 0.3, 1],
            [1, 0.3, 1, 1],
            [0.3, 1, 1, 1],
        ]
        anim = Animation(duration=0)
        for color in colors:
            anim += Animation(box_color=color, duration=0.3)
        anim.start(self)

    def play_all(self):
        self.bounce()
        self.spin()
        self.cycle_colors()
