import turtle
import random
from . import config
from .config import AlienType, Bounds
from .laser import Laser


class Alien:
    def __init__(self, bounds: Bounds, alien_type: AlienType, speed_mult: float = 1.0) -> None:
        self.bounds = bounds
        self.atype = alien_type
        self.hp = alien_type.hp
        self.points = alien_type.points
        self.speed = config.ALIEN_SPEED * alien_type.speed_mult * speed_mult
        self.fire_rate = config.ALIEN_FIRE_CHANCE_PER_SEC * alien_type.fire_mult
        self.alive = True

        self._t = turtle.Turtle()
        self._t.penup()
        self._t.shape(alien_type.shape)
        self._t.turtlesize(alien_type.size)
        self._t.color(*alien_type.color)
        self._t.setheading(270)
        self._t.setposition(
            random.randint(
                int(bounds.left + bounds.gutter),
                int(bounds.right - bounds.gutter),
            ),
            bounds.top,
        )

    @property
    def x(self) -> float:
        return self._t.xcor()

    @property
    def y(self) -> float:
        return self._t.ycor()

    def update(self, dt: float) -> None:
        self._t.forward(self.speed * dt)

    def maybe_fire(self, dt: float) -> Laser | None:
        if random.random() < self.fire_rate * dt:
            return Laser(self._t.xcor(), self._t.ycor() - 10, direction=-1)
        return None

    def hit(self) -> bool:
        self.hp -= 1
        if self.hp <= 0:
            return True
        # Brighten color as damage accumulates
        r, g, b = self.atype.color
        factor = 0.5 + 0.5 * (self.hp / self.atype.hp)
        self._t.color(
            min(1.0, r + (1 - r) * (1 - factor)),
            min(1.0, g + (1 - g) * (1 - factor)),
            min(1.0, b + (1 - b) * (1 - factor)),
        )
        return False

    def distance(self, x: float, y: float) -> float:
        return self._t.distance(x, y)

    def below_floor(self) -> bool:
        return self._t.ycor() < self.bounds.floor_level

    def destroy(self) -> None:
        self._t.clear()
        self._t.hideturtle()
        self.alive = False
