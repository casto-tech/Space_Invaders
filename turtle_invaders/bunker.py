import turtle
from . import config
from .laser import Laser


class BunkerBlock:
    def __init__(self, x: float, y: float) -> None:
        self._t = turtle.Turtle()
        self._t.penup()
        self._t.shape("square")
        self._t.turtlesize(
            config.BUNKER_BLOCK_SIZE / 20,
            config.BUNKER_BLOCK_SIZE / 20,
        )
        self._t.color(0.2, 0.8, 0.2)
        self._t.setposition(x, y)
        self._t.stamp()
        self._t.hideturtle()
        self.alive = True

    @property
    def x(self) -> float:
        return self._t.xcor()

    @property
    def y(self) -> float:
        return self._t.ycor()

    def distance(self, x: float, y: float) -> float:
        return self._t.distance(x, y)

    def destroy(self) -> None:
        self._t.clear()
        self._t.hideturtle()
        self.alive = False


class Bunker:
    def __init__(self, cx: float, cy: float) -> None:
        self.blocks: list[BunkerBlock] = []
        rows = config.BUNKER_BLOCK_ROWS
        cols = config.BUNKER_BLOCK_COLS
        bsize = config.BUNKER_BLOCK_SIZE
        spacing = bsize + 2
        for r in range(rows):
            for c in range(cols):
                x = cx + (c - cols // 2) * spacing
                y = cy + (r - rows // 2) * spacing
                self.blocks.append(BunkerBlock(x, y))

    def check_laser(self, laser: Laser) -> BunkerBlock | None:
        """Return the first block hit by laser, or None."""
        for block in self.blocks:
            if block.alive and block.distance(laser.x, laser.y) < config.BUNKER_BLOCK_SIZE * 1.5:
                return block
        return None

    def any_alive(self) -> bool:
        return any(b.alive for b in self.blocks)

    def destroy_all(self) -> None:
        for block in self.blocks:
            if block.alive:
                block.destroy()
