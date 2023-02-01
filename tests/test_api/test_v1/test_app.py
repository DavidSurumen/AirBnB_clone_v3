#!/usr/bin/python3
"""Testing the app module"""
from api.v1.app import app
import unittest
import json


class TestApp(unittest.TestCase):
    """Test cases for app"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_404(self):
        """Tests the error handler method"""
        ret_val = self.app.get('/bad')
        self.assertEqual(ret_val.status_code, 404)
        self.assertEqual(ret_val.headers.get("Content-Type"),
                         "application/json")

        json_format = json.loads(str(ret_val.get_data(), encoding="utf-8"))
        self.assertEqual(json_format.get("error"), "Not found")


if __name__ == '__main__':
    unittest.main()
