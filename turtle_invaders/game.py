import turtle
import tkinter
import random
import time
from enum import Enum, auto

from . import config
from .cannon import Cannon
from .alien import Alien
from .bunker import Bunker
from .hud import HUD
from . import scenes
from . import highscore


class State(Enum):
    START = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.title("SPACE INVADERS")
        self.screen.bgcolor(0.05, 0.05, 0.15)

        # Maximize the OS window, then resize the canvas to match so sprites
        # reach the edges.  bounds are computed after both steps.
        root = self.screen._root
        try:
            root.attributes("-zoomed", True)
        except Exception:
            try:
                root.state("zoomed")
            except Exception:
                pass
        root.update()

        # The turtle canvas widget doesn't auto-expand when the window is
        # maximized — resize it explicitly to the actual window dimensions.
        canvas = self.screen.getcanvas()
        canvas.config(width=root.winfo_width(), height=root.winfo_height())
        root.update()

        self.bounds = config.compute_bounds(self.screen)
        self.state = State.START
        self.high_score = highscore.load()

        # Game objects (populated on reset)
        self.cannon = None
        self.aliens = []
        self.player_lasers = []
        self.alien_lasers = []
        self.bunkers = []
        self.hud = None

        # Timers
        self.alien_spawn_timer = 0.0
        self.alien_spawn_interval = config.ALIEN_SPAWN_INTERVAL

        # Level / score state
        self.score = 0
        self.lives = config.STARTING_LIVES
        self.level = 1
        self.kills_this_level = 0
        self.alien_speed_mult = 1.0

        # Active overlay turtle
        self._overlay = None

        self._setup_keys()

    # ------------------------------------------------------------------
    # Key bindings
    # ------------------------------------------------------------------
    def _setup_keys(self):
        s = self.screen
        s.onkeypress(self._left_down, "Left")
        s.onkeyrelease(self._left_up, "Left")
        s.onkeypress(self._right_down, "Right")
        s.onkeyrelease(self._right_up, "Right")
        s.onkeypress(self._fire, "space")
        s.onkeypress(self._pause_toggle, "p")
        s.onkeypress(self._quit, "q")
        s.onkeypress(self._restart, "r")
        s.listen()

    def _left_down(self):
        if self.cannon:
            self.cannon.direction = -1

    def _left_up(self):
        if self.cannon and self.cannon.direction == -1:
            self.cannon.direction = 0

    def _right_down(self):
        if self.cannon:
            self.cannon.direction = 1

    def _right_up(self):
        if self.cannon and self.cannon.direction == 1:
            self.cannon.direction = 0

    def _fire(self):
        if self.state == State.START:
            self._start_game()
            return
        if self.state == State.PLAYING and self.cannon:
            laser = self.cannon.fire()
            if laser:
                self.player_lasers.append(laser)

    def _pause_toggle(self):
        if self.state == State.PLAYING:
            self.state = State.PAUSED
            self._overlay = scenes.draw_pause()
            self.screen.update()
        elif self.state == State.PAUSED:
            scenes.clear_overlay(self._overlay)
            self._overlay = None
            self.state = State.PLAYING
            self._last_frame_time = time.time()

    def _quit(self):
        turtle.bye()

    def _restart(self):
        if self.state == State.GAME_OVER:
            self._start_game()

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def _clear_all_sprites(self):
        if self.cannon:
            self.cannon.destroy()
            self.cannon = None
        for a in self.aliens:
            a.destroy()
        self.aliens.clear()
        for l in self.player_lasers:
            l.destroy()
        self.player_lasers.clear()
        for l in self.alien_lasers:
            l.destroy()
        self.alien_lasers.clear()
        for b in self.bunkers:
            b.destroy_all()
        self.bunkers.clear()
        if self.hud:
            self.hud.destroy()
            self.hud = None

    def _start_game(self):
        scenes.clear_overlay(self._overlay)
        self._overlay = None
        self._clear_all_sprites()

        self.score = 0
        self.lives = config.STARTING_LIVES
        self.level = 1
        self.kills_this_level = 0
        self.alien_speed_mult = 1.0
        self.alien_spawn_interval = config.ALIEN_SPAWN_INTERVAL
        self.alien_spawn_timer = 0.0

        self.cannon = Cannon(self.bounds)
        self.hud = HUD(self.bounds)

        # Place bunkers between cannon and mid-screen
        b = self.bounds
        bunker_y = b["FLOOR_LEVEL"] + (0 - b["FLOOR_LEVEL"]) * 0.4
        spacing = (b["RIGHT"] - b["LEFT"]) / (config.BUNKER_COUNT + 1)
        for i in range(config.BUNKER_COUNT):
            cx = b["LEFT"] + spacing * (i + 1)
            self.bunkers.append(Bunker(cx, bunker_y))

        self.state = State.PLAYING
        self._last_frame_time = time.time()

    def _advance_level(self):
        self.level += 1
        self.kills_this_level = 0
        self.alien_speed_mult *= config.LEVEL_SPEED_MULT
        self.alien_spawn_interval = max(
            0.3, self.alien_spawn_interval * config.LEVEL_SPAWN_MULT
        )

    def _kills_needed(self):
        return config.ALIENS_PER_LEVEL + 5 * (self.level - 1)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        self._overlay = scenes.draw_start()
        self.screen.update()

        while True:
            try:
                frame_start = time.time()

                if self.state in (State.START, State.PAUSED, State.GAME_OVER):
                    self.screen.update()  # flush tkinter events so key bindings fire
                    time.sleep(config.TIME_FOR_1_FRAME)
                    continue

                # PLAYING
                now = time.time()
                dt = now - self._last_frame_time
                self._last_frame_time = now
                dt = min(dt, 0.05)  # cap at 50ms to avoid huge jumps after pause

                self._update(dt)
                self.screen.update()

                elapsed = time.time() - frame_start
                if elapsed < config.TIME_FOR_1_FRAME:
                    time.sleep(config.TIME_FOR_1_FRAME - elapsed)

            except (turtle.Terminator, tkinter.TclError):
                break

    def _update(self, dt):
        self.cannon.update(dt)
        self.cannon.draw()

        # Spawn aliens
        self.alien_spawn_timer += dt
        if self.alien_spawn_timer >= self.alien_spawn_interval:
            self.alien_spawn_timer = 0.0
            atype = random.choice(config.ALIEN_TYPES)
            self.aliens.append(Alien(self.bounds, atype, self.alien_speed_mult))

        # Update aliens and collect new alien lasers
        new_alien_lasers = []
        for alien in self.aliens[:]:
            alien.update(dt)
            if alien.below_floor():
                alien.destroy()
                self.aliens.remove(alien)
                if self.cannon.hit():
                    self.lives -= 1
                    if self.lives <= 0:
                        self._end_game()
                        return
                continue
            laser = alien.maybe_fire(dt)
            if laser:
                new_alien_lasers.append(laser)
        self.alien_lasers.extend(new_alien_lasers)

        # Update player lasers
        for laser in self.player_lasers[:]:
            laser.update(dt)
            laser.draw()
            if laser.y > self.bounds["TOP"]:
                laser.destroy()
                self.player_lasers.remove(laser)
                continue
            # Check vs aliens
            hit_alien = False
            for alien in self.aliens[:]:
                if laser.distance(alien.x, alien.y) < 20:
                    laser.destroy()
                    self.player_lasers.remove(laser)
                    destroyed = alien.hit()
                    if destroyed:
                        alien.destroy()
                        self.aliens.remove(alien)
                        self.score += alien.points
                        self.kills_this_level += 1
                        if self.kills_this_level >= self._kills_needed():
                            self._advance_level()
                    hit_alien = True
                    break
            if hit_alien:
                continue
            # Check vs bunker blocks
            for bunker in self.bunkers:
                block = bunker.check_laser(laser)
                if block:
                    block.destroy()
                    laser.destroy()
                    self.player_lasers.remove(laser)
                    break

        # Update alien lasers
        for laser in self.alien_lasers[:]:
            laser.update(dt)
            laser.draw()
            if laser.y < self.bounds["BOTTOM"]:
                laser.destroy()
                self.alien_lasers.remove(laser)
                continue
            # Check vs cannon
            if laser.distance(self.cannon.x, self.cannon.y) < 25:
                laser.destroy()
                self.alien_lasers.remove(laser)
                if self.cannon.hit():
                    self.lives -= 1
                    if self.lives <= 0:
                        self._end_game()
                        return
                continue
            # Check vs bunker blocks
            for bunker in self.bunkers:
                block = bunker.check_laser(laser)
                if block:
                    block.destroy()
                    laser.destroy()
                    self.alien_lasers.remove(laser)
                    break

        self.hud.draw(self.score, self.high_score, self.lives, self.level)

    def _end_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            highscore.save(self.high_score)
        self._clear_all_sprites()
        self.state = State.GAME_OVER
        self._overlay = scenes.draw_game_over(self.score, self.high_score)
        self.screen.update()


def main():
    try:
        game = Game()
        game.run()
    except (turtle.Terminator, tkinter.TclError):
        pass
