# Submitter: katyh1(Huang, Katy)
# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


class Pulsator(Black_Hole):
    counter = 30

    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.time_between_meals = 0

    def update(self, model):
        prey_eat = Black_Hole.update(self, model)
        number_eat = len(prey_eat)
        self.time_between_meals += 1

        self.change_dimension(number_eat, number_eat)

        if self.time_between_meals % Pulsator.counter == 0:
            self.change_dimension(-1, -1)
        if self.get_dimension() == (0, 0):
            model.remove(self)
        return prey_eat
