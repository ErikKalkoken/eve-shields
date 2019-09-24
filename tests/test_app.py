# unittests for app module functions

import unittest
from unittest.mock import Mock, patch
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir + "/eveshields")
import json
import app
import bottle

class TestZkbStats(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # load test data
        with open("tests/test-data_zkb-stats.json", 'r', encoding="utf-8") as f:
            cls.stats = json.load(f)        
        
        # create mock get method to patch into requests
        mock = Mock()
        mock.json.return_value = cls.stats
        mock.raise_for_status = Mock()        
        cls.mock_get = mock
    
    @patch('app.requests.get')
    def test_activeP_pvp_chars(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'activePvpChars')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Active PVP chars',
            'message': '1.6k',
            'color': 'informational',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_corp_count(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'corpCount')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Corporations',
            'message': '66',
            'color': 'informational',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_danger_ratio(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'dangerRatio')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Danger',
            'message': 'Snuggly 55%',
            'color': 'green',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_isk_destroyed(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'iskDestroyed')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'ISK Destroyed',
            'message': '154.0t',
            'color': 'success',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_isk_lost(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'iskLost')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'ISK Lost',
            'message': '83.2t',
            'color': 'critical',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_isk_eff(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'iskEff')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'ISK Efficiency',
            'message': '65%',
            'color': 'success',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_member_count(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'memberCount')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Members',
            'message': '18.1k',
            'color': 'informational',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_ships_destroyed(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'shipsDestroyed')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Ships Destroyed',
            'message': '1.1m',
            'color': 'success',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_ships_lost(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'shipsLost')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Ships Lost',
            'message': '1.1m',
            'color': 'critical',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    @patch('app.requests.get')
    def test_ships_eff(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        x = app.zkb_stats('alliance', '0', 'shipsEff')
        self.assertDictEqual(json.loads(x), {
            'schemaVersion': 1,
            'label': 'Ships Efficiency',
            'message': '49%',
            'color': 'critical',
            'cacheSeconds': app.Shield.CACHE_SECONDS
        })

    # invalid properties should raise a HTTP error
    @patch('app.requests.get')
    def test_invalid_property(self, mock): 
        # replacing requests.get with mock method        
        mock.return_value = self.mock_get
        
        # performing tests                
        with self.assertRaises(bottle.HTTPError):
            x = app.zkb_stats('xyz', '0', 'shipsDestroyed')


class TestHelperFunctions(unittest.TestCase):
    
    def test_dict_safe_get(self):
        arr = {
            "one": 1,
            "two": 2,
            "more": {
                "three": 3,
                "four": 4,
                "more": {
                    "five": 5,
                    "six": 6           
        }}}
        
        # these should all work fine
        self.assertEqual(app._dict_safe_get(arr, "one"), 1)
        self.assertEqual(app._dict_safe_get(arr, "more", "three"), 3)        
        self.assertEqual(app._dict_safe_get(arr, "more", "more", "six"), 6)

        # these should raise errors
        with self.assertRaises(bottle.HTTPError):
            self.assertEqual(app._dict_safe_get(arr, "three"), 1)
        
        with self.assertRaises(bottle.HTTPError):
            self.assertEqual(app._dict_safe_get(arr, "more", "five"), 1)

        with self.assertRaises(bottle.HTTPError):
            self.assertEqual(app._dict_safe_get(arr, "more", "more", "one"), 1)



if __name__ == '__main__':
    unittest.main()