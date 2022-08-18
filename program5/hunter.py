# Submitter: katyh1(Huang, Katy)

# A Hunter class is derived from a Pulsator and then Mobile_Simulton base.
#   It inherits updating+displaying from Pusator/Mobile_Simulton: it pursues
#   any close prey, or moves in a straight line (see Mobile_Simultion).


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    constant_distance = 200

    def __init__(self, x, y):
        Pulsator.__init__(self, x, y)
        Mobile_Simulton.__init__(self, self.get_location()[0], self.get_location()[
                                 1], self.get_dimension()[0], self.get_dimension()[1], angle=0, speed=5)
        self.randomize_angle()

    def update(self, model):
        preys = model.find(lambda x: isinstance(x, Prey)
                           and self.distance(x.get_location()) <= Hunter.constant_distance)
        if len(preys) > 0:
            prey = sorted([p for p in preys],
                          key=lambda x: self.distance(x.get_location()))[0]
            px, py = prey.get_location()
            self.set_angle(atan2(py-self.get_location()[1], px-self.get_location()[
                0]))
            Pulsator.update(self, model)
            self.move()
