import turtle
import random
from . import config
from .laser import Laser


class Alien:
    def __init__(self, bounds, alien_type, speed_mult=1.0):
        self.bounds = bounds
        self.atype = alien_type
        self.hp = alien_type["hp"]
        self.points = alien_type["points"]
        self.speed = config.ALIEN_SPEED * alien_type["speed_mult"] * speed_mult
        self.fire_rate = config.ALIEN_FIRE_CHANCE_PER_SEC * alien_type["fire_mult"]
        self.alive = True

        self._t = turtle.Turtle()
        self._t.penup()
        self._t.shape(alien_type["shape"])
        self._t.turtlesize(alien_type["size"])
        self._t.color(*alien_type["color"])
        self._t.setheading(270)
        self._t.setposition(
            random.randint(
                int(bounds["LEFT"] + bounds["GUTTER"]),
                int(bounds["RIGHT"] - bounds["GUTTER"]),
            ),
            bounds["TOP"],
        )

    @property
    def x(self):
        return self._t.xcor()

    @property
    def y(self):
        return self._t.ycor()

    def update(self, dt):
        self._t.forward(self.speed * dt)

    def maybe_fire(self, dt):
        if random.random() < self.fire_rate * dt:
            return Laser(self._t.xcor(), self._t.ycor() - 10, direction=-1)
        return None

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            return True
        # Brighten color as damage accumulates
        r, g, b = self.atype["color"]
        factor = 0.5 + 0.5 * (self.hp / self.atype["hp"])
        self._t.color(
            min(1.0, r + (1 - r) * (1 - factor)),
            min(1.0, g + (1 - g) * (1 - factor)),
            min(1.0, b + (1 - b) * (1 - factor)),
        )
        return False

    def distance(self, x, y):
        return self._t.distance(x, y)

    def below_floor(self):
        return self._t.ycor() < self.bounds["FLOOR_LEVEL"]

    def destroy(self):
        self._t.clear()
        self._t.hideturtle()
        self.alive = False
