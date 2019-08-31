# unittest for Shield class

import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from app import Shield, _get_nested_dict_value


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
            "schemaVersion": "1",
            "label": "hi",
            "message": "sweet world",
            "color": "orange"
        })

    def test_format_isk(self):
        x = Shield("hi", "sweet world")
        self.assertEqual(x._format_isk(555), "555.0")
        self.assertEqual(x._format_isk(1570), "1.6k")
        self.assertEqual(x._format_isk(1570000), "1.6m")
        self.assertEqual(x._format_isk(1570000000), "1.6b")
        self.assertEqual(x._format_isk(1570000000000), "1.6t")

    def test_get_nested_dict_value(self):
        d = {
            "first": 1,
            "second": 2,
            "third": {
                "alpha": 5,
                "bravo": 6
            }
        }
        self.assertEqual(_get_nested_dict_value("first", d), 1)
        self.assertEqual(_get_nested_dict_value("second", d), 2)
        self.assertEqual(_get_nested_dict_value("third-alpha", d), 5)
        with self.assertRaises(KeyError):
            self.assertEqual(_get_nested_dict_value("xxx", d), 2)
        with self.assertRaises(KeyError):
            self.assertEqual(_get_nested_dict_value("third-xxx", d), 2)

if __name__ == '__main__':
    unittest.main()