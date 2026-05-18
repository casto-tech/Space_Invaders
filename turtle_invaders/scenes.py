import turtle


def _make_overlay():
    t = turtle.Turtle()
    t.penup()
    t.hideturtle()
    t.color(1, 1, 1)
    return t


def draw_start():
    t = _make_overlay()
    t.setposition(0, 60)
    t.write("SPACE INVADERS", font=("Courier", 36, "bold"), align="center")
    t.setposition(0, 0)
    t.write("Press SPACE to start", font=("Courier", 18, "normal"), align="center")
    t.setposition(0, -40)
    t.write(
        "Arrow keys: move   Space: fire   P: pause   Q: quit",
        font=("Courier", 12, "normal"),
        align="center",
    )
    return t


def draw_pause():
    t = _make_overlay()
    t.setposition(0, 20)
    t.write("PAUSED", font=("Courier", 40, "bold"), align="center")
    t.setposition(0, -30)
    t.write("Press P to resume", font=("Courier", 16, "normal"), align="center")
    return t


def draw_game_over(score, high_score):
    t = _make_overlay()
    t.setposition(0, 60)
    t.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
    t.setposition(0, 0)
    t.write(f"Score: {score}", font=("Courier", 22, "normal"), align="center")
    if score >= high_score and score > 0:
        t.setposition(0, -40)
        t.write("NEW HIGH SCORE!", font=("Courier", 18, "bold"), align="center")
    else:
        t.setposition(0, -40)
        t.write(f"Best: {high_score}", font=("Courier", 18, "normal"), align="center")
    t.setposition(0, -80)
    t.write("R: play again   Q: quit", font=("Courier", 14, "normal"), align="center")
    return t


def clear_overlay(overlay_turtle):
    if overlay_turtle is not None:
        overlay_turtle.clear()
        overlay_turtle.hideturtle()
