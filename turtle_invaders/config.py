FRAME_RATE = 60
TIME_FOR_1_FRAME = 1 / FRAME_RATE

CANNON_STEP = 200        # pixels per second
LASER_SPEED = 400        # pixels per second
LASER_LENGTH = 20
CANNON_FIRE_COOLDOWN = 0.3  # seconds between shots

STARTING_LIVES = 3
INVULN_DURATION = 1.5    # seconds of invulnerability after being hit

ALIEN_SPAWN_INTERVAL = 1.2   # seconds (scaled down each level)
ALIEN_SPEED = 60             # pixels per second (scaled up each level)
ALIEN_FIRE_CHANCE_PER_SEC = 0.25  # probability per alien per second

BUNKER_COUNT = 3
BUNKER_BLOCK_ROWS = 3
BUNKER_BLOCK_COLS = 7
BUNKER_BLOCK_SIZE = 10   # pixels

LEVEL_SPEED_MULT = 1.15
LEVEL_SPAWN_MULT = 0.85
ALIENS_PER_LEVEL = 10    # kills needed to advance (base; +5 per level)

# Each alien type: shape, size, points, speed_mult, hp, fire_mult
ALIEN_TYPES = [
    {
        "shape": "circle",
        "size": 1.0,
        "points": 10,
        "speed_mult": 1.0,
        "hp": 1,
        "fire_mult": 0.8,
        "color": (0.2, 0.9, 0.2),
    },
    {
        "shape": "square",
        "size": 1.4,
        "points": 20,
        "speed_mult": 0.75,
        "hp": 2,
        "fire_mult": 1.2,
        "color": (0.9, 0.6, 0.1),
    },
    {
        "shape": "turtle",
        "size": 1.8,
        "points": 30,
        "speed_mult": 0.5,
        "hp": 3,
        "fire_mult": 1.5,
        "color": (0.9, 0.2, 0.2),
    },
]


def compute_bounds(screen):
    w = screen.window_width()
    h = screen.window_height()
    left = -w / 2
    right = w / 2
    top = h / 2
    bottom = -h / 2
    floor_level = 0.9 * bottom
    gutter = 0.025 * w
    return {
        "LEFT": left,
        "RIGHT": right,
        "TOP": top,
        "BOTTOM": bottom,
        "FLOOR_LEVEL": floor_level,
        "GUTTER": gutter,
    }
