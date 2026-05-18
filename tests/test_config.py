import unittest
from turtle_invaders.config import AlienType, Bounds, compute_bounds, ALIEN_TYPES


class _MockScreen:
    def window_width(self) -> float:
        return 800.0

    def window_height(self) -> float:
        return 600.0


class TestComputeBounds(unittest.TestCase):
    def setUp(self):
        self.b = compute_bounds(_MockScreen())

    def test_horizontal_extents(self):
        self.assertEqual(self.b.left, -400.0)
        self.assertEqual(self.b.right, 400.0)

    def test_vertical_extents(self):
        self.assertEqual(self.b.top, 300.0)
        self.assertEqual(self.b.bottom, -300.0)

    def test_floor_level_below_bottom(self):
        self.assertLess(self.b.floor_level, 0)
        self.assertGreater(self.b.floor_level, self.b.bottom)

    def test_gutter_positive(self):
        self.assertGreater(self.b.gutter, 0)

    def test_bounds_is_frozen(self):
        with self.assertRaises(Exception):
            self.b.left = 0  # type: ignore[misc]


class TestAlienTypes(unittest.TestCase):
    def test_all_have_positive_hp(self):
        for atype in ALIEN_TYPES:
            self.assertGreater(atype.hp, 0, f"{atype.shape} hp must be > 0")

    def test_all_have_positive_points(self):
        for atype in ALIEN_TYPES:
            self.assertGreater(atype.points, 0)

    def test_all_have_valid_color(self):
        for atype in ALIEN_TYPES:
            for channel in atype.color:
                self.assertGreaterEqual(channel, 0.0)
                self.assertLessEqual(channel, 1.0)

    def test_alien_type_is_frozen(self):
        atype = ALIEN_TYPES[0]
        with self.assertRaises(Exception):
            atype.hp = 99  # type: ignore[misc]

    def test_three_types_defined(self):
        self.assertEqual(len(ALIEN_TYPES), 3)
