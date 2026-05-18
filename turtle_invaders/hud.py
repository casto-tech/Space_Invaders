import turtle


class HUD:
    def __init__(self, bounds):
        self.bounds = bounds
        self._text = turtle.Turtle()
        self._text.penup()
        self._text.hideturtle()
        self._text.color(1, 1, 1)

        # Life icon turtles (max 5)
        self._life_icons = []
        for _ in range(5):
            t = turtle.Turtle()
            t.penup()
            t.shape("square")
            t.color(1, 1, 1)
            t.turtlesize(0.6, 2.0)
            t.hideturtle()
            self._life_icons.append(t)

    def draw(self, score, high_score, lives, level):
        b = self.bounds
        self._text.clear()
        self._text.setposition(b["LEFT"] * 0.95, b["TOP"] * 0.85)
        self._text.write(
            f"Score: {score:5}   Hi: {high_score:5}   Level: {level}",
            font=("Courier", 16, "bold"),
        )

        # Draw life icons in top-right
        icon_x_start = b["RIGHT"] * 0.6
        icon_y = b["TOP"] * 0.88
        for i, icon in enumerate(self._life_icons):
            icon.clear()
            if i < lives:
                icon.setposition(icon_x_start + i * 30, icon_y)
                icon.showturtle()
                icon.stamp()
            else:
                icon.hideturtle()

    def clear(self):
        self._text.clear()
        for icon in self._life_icons:
            icon.clear()
            icon.hideturtle()

    def destroy(self):
        self.clear()
        self._text.hideturtle()
