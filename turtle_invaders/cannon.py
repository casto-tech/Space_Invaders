import turtle
from . import config
from .config import Bounds
from .laser import Laser


class Cannon:
    def __init__(self, bounds: Bounds) -> None:
        self.bounds = bounds
        self.direction = 0  # -1, 0, 1
        self._t = turtle.Turtle()
        self._t.penup()
        self._t.color(1, 1, 1)
        self._t.shape("square")
        self._t.setposition(0, bounds.floor_level)
        self.fire_cooldown = 0.0
        self.invuln_timer = 0.0
        self.alive = True

    @property
    def x(self) -> float:
        return self._t.xcor()

    @property
    def y(self) -> float:
        return self._t.ycor()

    def draw(self) -> None:
        self._t.clear()
        if self.invuln_timer > 0 and int(self.invuln_timer * 8) % 2 == 0:
            return  # flash during invulnerability
        fl = self.bounds.floor_level
        self._t.sety(fl)
        self._t.turtlesize(1, 4)
        self._t.stamp()
        self._t.sety(fl + 10)
        self._t.turtlesize(1, 1.5)
        self._t.stamp()
        self._t.sety(fl + 20)
        self._t.turtlesize(0.8, 0.3)
        self._t.stamp()
        self._t.sety(fl)

    def update(self, dt: float) -> None:
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        if self.invuln_timer > 0:
            self.invuln_timer -= dt

        left = self.bounds.left + self.bounds.gutter
        right = self.bounds.right - self.bounds.gutter
        new_x = self._t.xcor() + config.CANNON_STEP * self.direction * dt
        self._t.setx(max(left, min(right, new_x)))

    def fire(self) -> Laser | None:
        if self.fire_cooldown > 0:
            return None
        self.fire_cooldown = config.CANNON_FIRE_COOLDOWN
        return Laser(self._t.xcor(), self._t.ycor() + 20, direction=1)

    def hit(self) -> bool:
        if self.invuln_timer > 0:
            return False
        self.invuln_timer = config.INVULN_DURATION
        return True

    def reset(self) -> None:
        self._t.setposition(0, self.bounds.floor_level)
        self.direction = 0
        self.fire_cooldown = 0.0
        self.invuln_timer = 0.0

    def destroy(self) -> None:
        self._t.clear()
        self._t.hideturtle()
