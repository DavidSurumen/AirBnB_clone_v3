#!/usr/bin/python3
"""Test module for places_reviews view."""
import unittest
from models import storage
from api.v1.app import app
from models.review import Review
# to create a review, you must have a place and a user
from models.user import User
from models.place import Place
# to create a place, you must have a state and a city - which requires a state
from models.city import City
from models.state import State
import json


class TestPlacesReviewsView(unittest.TestCase):
    """Test cases for all routes in places_reviews.py module"""
    @classmethod
    def setUpClass(cls):
        """set up the flask app in testing mode, and create the\
        objects needed for the tests."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

        # create State object
        # create City object
        # create User object
        # create Place objec

    def test_get_reviews(self):
        """Test that a list of all review objects linked to a place object\
        is retrieved."""

    def test_get_reviews_bad_placeid(self):
        """Test that retrieving a list of review objects using a place id\
        that cannot be matched returns a 404."""

    def test_get_review(self):
        """Test that a single review object is retrieved."""

    def test_get_review_bad_review_id(self):
        """Test that retrieving a review object using an id that is not\
        matched returns a 404."""

    def test_delete_review(self):
        """Test that a review object is deleted."""

    def test_delete_review_bad_review_id(self):
        """Test that deleting a review object whose id is not in storage\
        returns a 404."""

    def test_create_review(self):
        """Test that a review object is created."""

    def test_create_review_bad_place_id(self):
        """Test that creating a review object for a place id that is not\
        in storage returns a 404."""

    def test_create_review_bad_json(self):
        """Test that creating a review object with a request that is not\
        valid json returns 400 with 'Not a JSON'"""

    def test_create_review_bad_user_id(self):
        """Test that creating a review object using a user id that is\
        not matched by any user object in storage returns 404"""

    def test_create_review_no_user_id(self):
        """Test that creating a review object with a request that does not\
        contain user id returns 400 with 'Missing user_id'"""

    def test_create_review_no_text(self):
        """Test that creating a review object with a request that does not\
        contain the key 'text' returns 400 with 'Missing text'"""

    def test_update_review(self):
        """Test that an existing review object is updated."""

    def test_update_review_bad_review_id(self):
        """Test that updating a review object with an id that is not matched\
        in storage returns a 404."""

    def test_update_review_bad_json(self):
        """Test that updating a review object with data that is not valid\
        json returns 400 with 'Not a JSON'"""

    def test_update_review_skipped_some_attributes(self):
        """Test that updating a review object leaves id, created_at, user_id,\
        place_id, and updated_at unchanged."""
    
    @classmethod
    def tearDownClass(cls):
        """destroy the objects created in setUp"""
        # delete state -> which deletes cities -> which deletes places
        # -> which deletes reviews
        # delete user -> which deletes reviews
