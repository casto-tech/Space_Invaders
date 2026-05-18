import turtle
import tkinter
import random
import time
from enum import Enum, auto

from . import config
from .config import Bounds
from .cannon import Cannon
from .alien import Alien
from .bunker import Bunker
from .hud import HUD
from .laser import Laser
from . import scenes
from . import highscore


class State(Enum):
    START = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.title("SPACE INVADERS")
        self.screen.bgcolor(0.05, 0.05, 0.15)

        self._maximize_window()

        self.bounds: Bounds = config.compute_bounds(self.screen)
        self.state = State.START
        self.high_score = highscore.load()

        self.cannon: Cannon | None = None
        self.aliens: list[Alien] = []
        self.player_lasers: list[Laser] = []
        self.alien_lasers: list[Laser] = []
        self.bunkers: list[Bunker] = []
        self.hud: HUD | None = None

        self.alien_spawn_timer = 0.0
        self.alien_spawn_interval = config.ALIEN_SPAWN_INTERVAL

        self.score = 0
        self.lives = config.STARTING_LIVES
        self.level = 1
        self.kills_this_level = 0
        self.alien_speed_mult = 1.0

        self._overlay: turtle.Turtle | None = None
        self._last_frame_time = 0.0

        self._setup_keys()

    def _maximize_window(self) -> None:
        root = self.screen._root
        # Try Linux first, fall back to Windows/macOS state("zoomed")
        try:
            root.attributes("-zoomed", True)
        except tkinter.TclError:
            try:
                root.state("zoomed")
            except tkinter.TclError:
                pass
        root.update()
        canvas = self.screen.getcanvas()
        canvas.config(width=root.winfo_width(), height=root.winfo_height())
        root.update()

    # ------------------------------------------------------------------
    # Key bindings
    # ------------------------------------------------------------------
    def _setup_keys(self) -> None:
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

    def _left_down(self) -> None:
        if self.cannon:
            self.cannon.direction = -1

    def _left_up(self) -> None:
        if self.cannon and self.cannon.direction == -1:
            self.cannon.direction = 0

    def _right_down(self) -> None:
        if self.cannon:
            self.cannon.direction = 1

    def _right_up(self) -> None:
        if self.cannon and self.cannon.direction == 1:
            self.cannon.direction = 0

    def _fire(self) -> None:
        if self.state == State.START:
            self._start_game()
            return
        if self.state == State.PLAYING and self.cannon:
            laser = self.cannon.fire()
            if laser:
                self.player_lasers.append(laser)

    def _pause_toggle(self) -> None:
        if self.state == State.PLAYING:
            self.state = State.PAUSED
            self._overlay = scenes.draw_pause()
            self.screen.update()
        elif self.state == State.PAUSED:
            scenes.clear_overlay(self._overlay)
            self._overlay = None
            self.state = State.PLAYING
            self._last_frame_time = time.time()

    def _quit(self) -> None:
        turtle.bye()

    def _restart(self) -> None:
        if self.state == State.GAME_OVER:
            self._start_game()

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def _clear_all_sprites(self) -> None:
        if self.cannon:
            self.cannon.destroy()
            self.cannon = None
        for a in self.aliens:
            a.destroy()
        self.aliens.clear()
        for laser in self.player_lasers:
            laser.destroy()
        self.player_lasers.clear()
        for laser in self.alien_lasers:
            laser.destroy()
        self.alien_lasers.clear()
        for b in self.bunkers:
            b.destroy_all()
        self.bunkers.clear()
        if self.hud:
            self.hud.destroy()
            self.hud = None

    def _start_game(self) -> None:
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

        b = self.bounds
        bunker_y = b.floor_level + (0 - b.floor_level) * 0.4
        spacing = (b.right - b.left) / (config.BUNKER_COUNT + 1)
        for i in range(config.BUNKER_COUNT):
            cx = b.left + spacing * (i + 1)
            self.bunkers.append(Bunker(cx, bunker_y))

        self.state = State.PLAYING
        self._last_frame_time = time.time()

    def _advance_level(self) -> None:
        self.level += 1
        self.kills_this_level = 0
        self.alien_speed_mult *= config.LEVEL_SPEED_MULT
        self.alien_spawn_interval = max(
            0.3, self.alien_spawn_interval * config.LEVEL_SPAWN_MULT
        )

    def _kills_needed(self) -> int:
        return config.ALIENS_PER_LEVEL + 5 * (self.level - 1)

    def _end_game(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            highscore.save(self.high_score)
        self._clear_all_sprites()
        self.state = State.GAME_OVER
        self._overlay = scenes.draw_game_over(self.score, self.high_score)
        self.screen.update()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        self._overlay = scenes.draw_start()
        self.screen.update()

        while True:
            try:
                frame_start = time.time()

                if self.state in (State.START, State.PAUSED, State.GAME_OVER):
                    self.screen.update()
                    time.sleep(config.TIME_FOR_1_FRAME)
                    continue

                now = time.time()
                dt = min(now - self._last_frame_time, 0.05)
                self._last_frame_time = now

                self._update(dt)
                self.screen.update()

                elapsed = time.time() - frame_start
                if elapsed < config.TIME_FOR_1_FRAME:
                    time.sleep(config.TIME_FOR_1_FRAME - elapsed)

            except (turtle.Terminator, tkinter.TclError):
                break

    # ------------------------------------------------------------------
    # Per-frame update (split into focused helpers)
    # ------------------------------------------------------------------
    def _update(self, dt: float) -> None:
        assert self.cannon is not None
        assert self.hud is not None
        self.cannon.update(dt)
        self.cannon.draw()
        self._spawn_alien(dt)
        self._update_aliens(dt)
        if self.state is not State.PLAYING:
            return
        self._process_player_lasers(dt)
        self._process_alien_lasers(dt)
        if self.state is not State.PLAYING:
            return
        self.hud.draw(self.score, self.high_score, self.lives, self.level)

    def _spawn_alien(self, dt: float) -> None:
        self.alien_spawn_timer += dt
        if self.alien_spawn_timer >= self.alien_spawn_interval:
            self.alien_spawn_timer = 0.0
            atype = random.choice(config.ALIEN_TYPES)
            self.aliens.append(Alien(self.bounds, atype, self.alien_speed_mult))

    def _update_aliens(self, dt: float) -> None:
        assert self.cannon is not None
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
                self.alien_lasers.append(laser)

    def _process_player_lasers(self, dt: float) -> None:
        for laser in self.player_lasers[:]:
            laser.update(dt)
            laser.draw()
            if laser.y > self.bounds.top:
                laser.destroy()
                self.player_lasers.remove(laser)
                continue
            if self._player_laser_hits_alien(laser):
                continue
            self._player_laser_hits_bunker(laser)

    def _player_laser_hits_alien(self, laser: Laser) -> bool:
        for alien in self.aliens[:]:
            if laser.distance(alien.x, alien.y) < 20:
                laser.destroy()
                self.player_lasers.remove(laser)
                if alien.hit():
                    alien.destroy()
                    self.aliens.remove(alien)
                    self.score += alien.points
                    self.kills_this_level += 1
                    if self.kills_this_level >= self._kills_needed():
                        self._advance_level()
                return True
        return False

    def _player_laser_hits_bunker(self, laser: Laser) -> None:
        for bunker in self.bunkers:
            block = bunker.check_laser(laser)
            if block:
                block.destroy()
                laser.destroy()
                self.player_lasers.remove(laser)
                break

    def _process_alien_lasers(self, dt: float) -> None:
        for laser in self.alien_lasers[:]:
            laser.update(dt)
            laser.draw()
            if laser.y < self.bounds.bottom:
                laser.destroy()
                self.alien_lasers.remove(laser)
                continue
            if self._alien_laser_hits_cannon(laser):
                if self.state is not State.PLAYING:
                    return
                continue
            self._alien_laser_hits_bunker(laser)

    def _alien_laser_hits_cannon(self, laser: Laser) -> bool:
        assert self.cannon is not None
        if laser.distance(self.cannon.x, self.cannon.y) < 25:
            laser.destroy()
            self.alien_lasers.remove(laser)
            if self.cannon.hit():
                self.lives -= 1
                if self.lives <= 0:
                    self._end_game()
            return True
        return False

    def _alien_laser_hits_bunker(self, laser: Laser) -> None:
        for bunker in self.bunkers:
            block = bunker.check_laser(laser)
            if block:
                block.destroy()
                laser.destroy()
                self.alien_lasers.remove(laser)
                break


def main() -> None:
    try:
        game = Game()
        game.run()
    except (turtle.Terminator, tkinter.TclError):
        pass
