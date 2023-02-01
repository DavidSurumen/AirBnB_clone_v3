#!/usr/bin/python3
"""Testing index view"""
from api.v1.app import app
import unittest
import json


def getJson(response):
    """
    Extract the json dictionary from a flask response object.
    """
    return json.loads(str(response.get_data(), encoding='utf-8'))


class TestIndex(unittest.TestCase):
    """Test cases for all routes in index.py"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_status(self):
        """Tests that the route /status returns status OK with code 200"""
        ret = self.app.get('{}/status/'.format(self.path))

        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers.get('Content-Type'), 'application/json')

        json_format = getJson(ret)
        self.assertEqual(json_format.get('status'), 'OK')

    def test_stats(self):
        """Tests that the route /stats returns the number of objects in
        storage by type, and code 200"""
        ret = self.app.get('{}/stats/'.format(self.path))

        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers.get("Content-Type"), "application/json")

        json_format = getJson(ret)
        for typ in ["users", "reviews", "cities", "states", "places",
                    "amenities"]:
            self.assertIn(typ, json_format.keys())


if __name__ == "__main__":
    unittest.main()
