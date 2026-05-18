import turtle
from . import config


class Laser:
    def __init__(self, x: float, y: float, direction: int = 1) -> None:
        """direction: 1 = up (player), -1 = down (alien)"""
        self.direction = direction
        self._t = turtle.Turtle()
        self._t.penup()
        self._t.hideturtle()
        if direction == 1:
            self._t.color(1, 0.2, 0.2)
        else:
            self._t.color(0.2, 1, 0.8)
        self._t.setposition(x, y)
        self._t.setheading(90 if direction == 1 else 270)
        self._t.pensize(3)
        self.alive = True

    @property
    def x(self) -> float:
        return self._t.xcor()

    @property
    def y(self) -> float:
        return self._t.ycor()

    def draw(self) -> None:
        self._t.clear()
        self._t.pendown()
        self._t.forward(config.LASER_LENGTH)
        self._t.forward(-config.LASER_LENGTH)
        self._t.penup()

    def update(self, dt: float) -> None:
        self._t.forward(config.LASER_SPEED * dt)

    def distance(self, x: float, y: float) -> float:
        return self._t.distance(x, y)

    def destroy(self) -> None:
        self._t.clear()
        self._t.hideturtle()
        self.alive = False
