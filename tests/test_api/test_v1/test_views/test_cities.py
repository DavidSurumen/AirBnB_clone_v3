#!/usr/bin/python3
"""Test module for Cities view."""
import unittest
from api.v1.app import app
from models import storage
from models.state import State
from models.city import City
from models import storage
import json


class TestCitiesViews(unittest.TestCase):
    """Test cases for all routes in cities.py"""
    @classmethod
    def setUpClass(cls):
        """set the flask app in testing mode."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

    def test_get_state_cities(self):
        """Test that all cities of a state are retrieved correctly."""
        st = {'name': 'MyNewState', 'id': 'lil-state-id-0'}
        state = State(**st)
        state.save()

        city = {'name': 'Nairobi', 'state_id': state.id}
        city = City(**city)
        city.save()

        city2 = {'name': 'Mombasa', 'state_id': state.id}
        city2 = City(**city2)
        city2.save()

        res = self.app.get('/api/v1/states/{}/cities'.format(state.id))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_formt = json.loads(str(res.get_data(), encoding="utf-8"))
        for ct in json_formt:
            self.assertEqual(ct["state_id"], st["id"])

        storage.delete(state)

    def test_get_state_cities_unmatched_state_id(self):
        """Test that getting cities of a state that does not exist returns
        404."""
        state_args = {'name': "OldState1"}
        state_ob = State(**state_args)
        state_ob.save()

        city1 = {'name': "SitiOne1", 'state_id': state_ob.id}
        city1 = City(**city1)
        city1.save()

        city2 = {'name': 'SitiTwo', 'state_id': state_ob.id}
        city2 = City(**city2)
        city2.save()

        res = self.app.get('/api/v1/states/fake-sk495-state-sr341-id/cities')
        self.assertEqual(res.status_code, 404)

        storage.delete(state_ob)

    def test_get_city(self):
        """Test that a single City object can be retrieved correctly."""
        state = {"name": "OldState2", "id": "lil-old-state-23"}
        state = State(**state)
        state.save()

        cit1 = {'name': 'SitiOne2', 'state_id': state.id}
        cit1 = City(**cit1)
        cit1.save()

        res = self.app.get('/api/v1/cities/{}'.format(cit1.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

        json_format = json.loads(str(res.get_data(), encoding='utf-8'))
        self.assertTrue(type(json_format), list)
        storage.delete(state)

    def test_get_city_umatched_cityid(self):
        """Test that retrieving a city object with an id that doesn't exist\
                returns 404."""
        st_args = {'name': 'Dummy', 'id': 'false-id'}
        state = State(**st_args)
        state.save()

        cit = {'name': 'Dummy', 'state_id': state.id}
        cit = City(**cit)
        cit.save()

        res = self.app.get('/api/v1/cities/a-really-fake-city-id')
        self.assertEqual(res.status_code, 404)

        storage.delete(state)

    def test_delete_city(self):
        """Test that a city object is correctly deleted."""
        st_args = {'name': 'Dummy State'}
        state = State(**st_args)
        state.save()

        cit = {'name': 'Fake City', 'state_id': state.id}
        cit = City(**cit)
        cit.save()

        self.assertIsNotNone(storage.get(City, cit.id))

        res = self.app.delete('/api/v1/cities/{}'.format(cit.id))
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json, {})

        self.assertIsNone(storage.get(City, cit.id))
        storage.delete(state)

    def test_delete_city_wrong_id(self):
        """Test that deleting a city object whose id does not match any in
        storage returns 404."""
        state = {'name': 'OldDummyState'}
        state = State(**state)
        state.save()

        cit = {'name': 'SomeCity', 'state_id': state.id}
        cit = City(**cit)
        cit.save()

        self.assertIsNotNone(storage.get(City, cit.id))
        res = self.app.delete('/api/v1/cities/some-fake-city-id')
        self.assertEqual(res.status_code, 404)
        self.assertIsNotNone(storage.get(City, cit.id))
        storage.delete(state)

    @unittest.skip
    def test_create_city(self):
        """Test that a new city object can be correctly created."""
        state_args = {'name': 'BigState', 'id': 'small-id-0'}
        state = State(**state_args)
        state.save()

        city_args = {'name': 'Capitol', 'population': 'Big'}
        res = self.app.post('/api/v1/states/{}/cities'.format(state.id),
                            json=city_args)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

        json_city = json.loads(str(res.get_data(), encoding='utf-8'))
        self.assertEqual(json_city.get("name"), city_args["name"])
        self.assertEqual(json_city.get("state_id"), state.id)
        self.assertIsNotNone(storage.get(City, json_city['id']))
        storage.delete(state)

    @unittest.skip
    def test_create_city_bad_state_id(self):
        """Test the attempting to create a City obj with unmatching state id\
        causes a 404."""
        city_args = {'name': 'NoCity'}
        res = self.app.post('/api/v1/states/no-city-ir5igt-10/cities',
                            json=city_args)
        self.assertEqual(res.status_code, 404)
    
    @unittest.skip
    def test_create_city_no_name(self):
        """Test that creating a City object without giving its name in the\
        request returns a 400 with 'Missing name'"""
        state = {'name': 'NewState'}
        state = State(**state)
        state.save()

        cit_args = {'amenities': 'Good'}
        res = self.app.post('/api/v1/states/{}/cities'.format(state.id),
                            json=cit_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Missing name")
        storage.delete(state)

    def test_create_city_bad_json(self):
        """Test that creating a City object with request data that is not\
        valid json returns a 400 with 'Not a JSON'"""
        state = {'name': 'Other State'}
        state = State(**state)
        state.save()

        # data that is not JSON Serializable
        cit_args = ['name', 'Not Known']
        res = self.app.post('/api/v1/states/{}/cities'.format(state.id),
                            json=cit_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Not a JSON")

        # 'Content-Type' of header not 'application/json'
        cit_args = {'name': 'Not Known'}
        res = self.app.post('/api/v1/states/{}/cities'.format(state.id),
                            content_type='application/image',
                            data=json.dumps(cit_args))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Not a JSON")
        storage.delete(state)

    def test_update_city(self):
        """Test that a City object is correctly updated."""
        state = {'name': 'MyState'}
        state = State(**state)
        state.save()

        ct = {'name': 'MyCity', 'state_id': state.id}
        cty = City(**ct)
        cty.save()

        new_dat = {'name': 'Joburg'}
        res = self.app.put('/api/v1/cities/{}'.format(cty.id),
                            json=new_dat)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

        self.assertEqual(res.json.get('name'), new_dat['name'])
        storage.delete(state)

    def test_update_city_bad_city_id(self):
        """Test that updating a city object with an id that is umatched
        returns a 404."""
        state = {'name': 'MyState'}
        state = State(**state)
        state.save()

        cty = {'name': 'MyCity', 'state_id': state.id}
        cty = City(**cty)
        cty.save()

        new = {'name': 'ZeroCity'}
        res = self.app.put('/api/v1/cities/this-id-zero-9',
                           json=new)
        self.assertEqual(res.status_code, 404)
        storage.delete(state)

    def test_update_city_bad_json(self):
        """Test that updating a city obj with invalid json returns a 400 with\
        the message 'Not a JSON'"""
        state = {'name': 'MyState'}
        state = State(**state)
        state.save()

        cty = {'name': 'MyCty', 'state_id': state.id}
        cty = City(**cty)
        cty.save()

        bad_json = 'This is a String'
        res = self.app.put('/api/v1/cities/{}'.format(cty.id),
                           content_type='application/json',
                           data=json.dumps(bad_json))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Not a JSON")
        storage.delete(state)
