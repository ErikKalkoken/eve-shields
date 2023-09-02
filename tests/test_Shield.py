# unittest for Shield class

import unittest

from eveshields.app import Shield


class TestShield(unittest.TestCase):
    def test_create_minimal(self):
        x = Shield("hi", "sweet world")
        self.assertEqual(x.label, "hi")
        self.assertEqual(x.message, "sweet world")
        self.assertIsNone(x.color)
        self.assertIsNone(x.format)

    def test_create_full(self):
        x = Shield("hi", "sweet world", "orange", "isk")
        self.assertEqual(x.label, "hi")
        self.assertEqual(x.message, "sweet world")
        self.assertEqual(x.color, "orange")
        self.assertEqual(x.format, "isk")

    def test_setters1(self):
        x = Shield("hi", "sweet world")
        self.assertEqual(x.label, "hi")
        x.label = 1
        self.assertEqual(x.label, "1")
        x.message = 99
        self.assertEqual(x.message, 99)
        x.color = "red"
        self.assertEqual(x.color, "red")
        x.format = "isk"
        self.assertEqual(x.format, "isk")

    def test_set_message(self):
        x = Shield("hi", "sweet world", "orange", "isk")
        with self.assertRaises(ValueError):
            x.message = None
        with self.assertRaises(ValueError):
            x.message = ""

    def test_set_format(self):
        x = Shield("hi", "sweet world")
        with self.assertRaises(ValueError):
            x.format = "xyz"

    def test_get_dict(self):
        x = Shield("hi", "sweet world", "orange")
        self.assertDictEqual(
            x.get_api_dict(),
            {
                "schemaVersion": 1,
                "label": "hi",
                "message": "sweet world",
                "color": "orange",
                "cacheSeconds": Shield.CACHE_SECONDS,
            },
        )

    def test__format_number(self):
        x = Shield("hi", "sweet world")
        self.assertEqual(x._format_number(555), "555")
        self.assertEqual(x._format_number(1570), "1.6k")
        self.assertEqual(x._format_number(1570000), "1.6m")
        self.assertEqual(x._format_number(1570000000), "1.6b")
        self.assertEqual(x._format_number(1570000000000), "1.6t")


if __name__ == "__main__":
    unittest.main()
