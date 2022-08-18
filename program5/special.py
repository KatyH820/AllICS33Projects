
from prey import Prey
import random

# My special class create ball that will randomly change color from the available color list


class Special(Prey):
    radius = 5

    def __init__(self, x, y):
        super().__init__(x, y, width=5, height=5, angle=0, speed=5)
        self.randomize_angle()

    def update(self, model):
        self.move()

    def display(self, canvas):
        color = ['red', 'purple', 'yellow', 'green', 'blue', 'orange',
                 'brown', 'black', 'pink', 'coral']
        num = random.randint(0, 9)
        canvas.create_oval(self._x-Special.radius, self._y-Special.radius,
                           self._x+Special.radius, self._y+Special.radius,
                           fill=color[num])
