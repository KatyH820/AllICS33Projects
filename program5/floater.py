# Submitter: katyh1(Huang, Katy)

# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


#from PIL.ImageTk import PhotoImage
from prey import Prey
import random


class Floater(Prey):
    radius = 5

    def __init__(self, x, y):
        Prey.__init__(self, x, y, width=10, height=10, angle=0, speed=5)
        self.randomize_angle()

    def update(self, model):
        n = random.uniform(-0.5, 0.5)
        if 0 <= random.random() <= 0.3:
            self.set_angle(self.get_angle()+n)
            if 3 <= self._speed+n <= 7:
                self.set_speed(self._speed+n)
            else:
                if self._speed+n <= 3:
                    self.set_speed(3)
                elif self._speed+n >= 7:
                    self.set_speed(7)
        self.move()

    def display(self, canvas):
        canvas.create_oval(self._x-Floater.radius, self._y-Floater.radius,
                           self._x+Floater.radius, self._y+Floater.radius,
                           fill="red")
