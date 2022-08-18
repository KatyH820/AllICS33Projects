# A Black_Hole is derived from a Simulton base; it updates by finding+removing
#   any objects (derived from a Prey base) whose center is crosses inside its
#   radius (and returns a set of all eaten simultons); it displays as a black
#   circle with a radius of 10 (e.g., a width/height 20).
# Calling get_dimension for the width/height (for containment and displaying)'
#   will facilitate inheritance in Pulsator and Hunter

# Submitter: katyh1(Huang, Katy)
from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    radius = 10

    def __init__(self, x, y):
        Simulton.__init__(self, x, y, width=20, height=20)

    def update(self, model):
        preys = model.find(lambda x: isinstance(x, Prey))
        eaten = set()
        for b in preys:
            if self.contains(b.get_location()):
                model.remove(b)
                eaten.add(b)
        return eaten

    def display(self, canvas):
        canvas.create_oval(self._x-self._width/2, self._y-self._width/2,
                           self._x+self._width/2, self._y+self._width/2,
                           fill='black')

    def contains(self, location):
        return self.distance(location) < Black_Hole.radius
