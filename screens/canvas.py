import random
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty

from app import BaseScreen


class CanvasScreen(BaseScreen):
    shape_color = ListProperty([0.2, 0.6, 1, 1])
    shape_rotation = NumericProperty(0)

    def randomize_color(self):
        self.shape_color = [random.random(), random.random(), random.random(), 1]

    def rotate_shape(self):
        anim = Animation(shape_rotation=self.shape_rotation + 45, duration=0.3, t="out_back")
        anim.start(self)
