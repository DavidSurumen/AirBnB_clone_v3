#!/usr/bin/python3
"""Test module for Places view."""
import unittest
from models import storage
from api.v1.app import app
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
import json


class TestPlacesViews(unittest.TestCase):
    """Test cases for all routes in places.py."""
    @classmethod
    def setUpClass(cls):
        """set up the flask app in testing mode."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

        """Create the objects need for tests"""
        cls.state = {'name': 'MyState'}
        cls.state = State(**cls.state)
        cls.state.save()

        cls.city = {'name': 'MyCity', 'state_id': cls.state.id}
        cls.city = City(**cls.city)
        cls.city.save()

        cls.user = {'email': 'email@user1', 'password': 'pass1'}
        cls.user = User(**cls.user)
        cls.user.save()

    def test_get_city_places(self):
        """Test that a list of all Place objects of a City in storage can be\
        correctly retrieved."""
        place_args = {'city_id': self.city.id, 'user_id': self.user.id,
                      'name': 'Dukuya'}
        place = Place(**place_args)
        place.save()

        res = self.app.get('/api/v1/cities/{}/places'.format(self.city.id))
        self.assertEqual(res.status_code, 200)
        ls_places = res.json
        for plc in ls_places:
            self.assertEqual(plc['name'], 'Dukuya')
        storage.delete(place)

    def test_get_city_places_wrong_id(self):
        """Test that listing places objects with unmatched city id returns a
        404."""
        res = self.app.get('/api/v1/cities/fake-city-id-39l/places')
        self.assertEqual(res.status_code, 404)

    def test_get_place(self):
        """Test that single place object can be retrieved."""
        place_args = {'city_id': self.city.id, 'user_id': self.user.id,
                      'name': 'Siadi'}
        place = Place(**place_args)
        place.save()

        res = self.app.get('/api/v1/places/{}'.format(place.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, place.to_dict())
        storage.delete(place)

    def test_get_place_bad_id(self):
        """Test that retrieving a single place object with unmatched id\
        returns a 404."""
        res = self.app.get('/api/v1/places/no-id-like-this-092,')
        self.assertEqual(res.status_code, 404)

    def test_delete_place(self):
        """Test that a place object is deleted."""
        place_args = {'name': 'Deleted', 'city_id': self.city.id,
                      'user_id': self.user.id}
        place = Place(**place_args)
        place.save()

        self.assertIsNotNone(storage.get(Place, place.id))
        res = self.app.delete('/api/v1/places/{}'.format(place.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {})
        self.assertIsNone(storage.get(Place, place.id))
        storage.delete(place)

    def test_delete_place_bad_id(self):
        """Test that deleting a place object with an invalid id returns a 404.
        """
        res = self.app.delete('/api/v1/places/not-a-real-id-2002')
        self.assertEqual(res.status_code, 404)

    def test_update_place(self):
        """Test that a place object is updated."""
        plac_ags = {'name': 'NewPlace', 'city_id': self.city.id,
                    'user_id': self.user.id}
        place = Place(**plac_ags)
        place.save()

        self.assertEqual(storage.get(Place, place.id).name, plac_ags['name'])
        new_dat = {'name': 'OldPlace', 'city_id': 'MovedCity'}
        res = self.app.put('/api/v1/places/{}'.format(place.id),
                           json=new_dat)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('name'), new_dat['name'])
        self.assertEqual(res.json.get('city_id'), plac_ags['city_id'])

    def test_update_place_bad_id(self):
        """Test that updating a place object while passing unmatching id\
        reurns a 404."""
        data = {'name': 'FailedPlace'}
        res = self.app.put('/api/v1/places/a-lil-place-02k4',
                           json=data)
        self.assertEqual(res.status_code, 404)

    def test_update_place_bad_json(self):
        """Test that updating a place object with data that is not valid\
        json returns a 400 with 'Not a JSON'"""
        place = {'name': 'NewPlace', 'city_id': self.city.id,
                 'user_id': self.user.id}
        place = Place(**place)
        place.save()

        new_dat = ('Invalid', 'Json')
        res = self.app.put('/api/v1/places/{}'.format(place.id),
                           json=new_dat)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')

    @classmethod
    def tearDownClass(cls):
        """Clean up objects created in setUp"""
        storage.delete(cls.state)
        storage.delete(cls.user)
