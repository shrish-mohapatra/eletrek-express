from .shape import Shape


class Station(Shape):
    def __init__(self, id, shape, x, y):
        self.id = id
        self.shape = shape
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.id} - {self.shape_str()} - ({self.x},{self.y})'
