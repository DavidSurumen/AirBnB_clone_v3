#!/usr/bin/python3
"""Test module for Amenities view."""
import unittest
from api.v1.app import app
from models.amenity import Amenity
from models import storage
import json


class TestAmenityView(unittest.TestCase):
    """Test Cases for all the routes in the amenities.py module."""
    @classmethod
    def setUpClass(cls):
        """set up the flask app in testing mode."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

    def test_get_amenities(self):
        """Test that all amenities objects are retrieved."""
        ame1 = {'name': 'WiFi'}
        ame1 = Amenity(**ame1)
        ame1.save()

        res = self.app.get('/api/v1/amenities')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

        self.assertTrue(type(res.json), list)
        self.assertIn(ame1.name, [am.get('name') for am in res.json])
        self.assertIsNotNone(storage.get(Amenity, ame1.id))
        storage.delete(ame1)

    def test_get_amenities_specific(self):
        """Test retrieving an amenity using its id."""
        ame2 = {'name': 'Gym'}
        ame2 = Amenity(**ame2)
        ame2.save()

        res = self.app.get('/api/v1/amenities/{}'.format(ame2.id))
        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.json.get('name'), ame2.name)
        storage.delete(ame2)

    def test_get_amenity_bad_id(self):
        """Test that retrieving an amenity using an unmatched id returns a 404
        """
        ame3 = {'name': 'Pap'}
        ame3 = Amenity(**ame3)
        ame3.save()

        res = self.app.get('/api/v1/amenities/really-false-id-here')
        self.assertEqual(res.status_code, 404)
        self.assertIsNotNone(storage.get(Amenity, ame3.id))
        storage.delete(ame3)

    def test_delete_amenity(self):
        """Test that an amenity object is correctly deleted from storage."""
        ame4 = {'name': 'To Delete'}
        ame4 = Amenity(**ame4)
        ame4.save()

        res = self.app.delete('/api/v1/amenities/{}'.format(ame4.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {})

    def test_delete_amenity_bad_id(self):
        """Test that attempting to delete an amenity with an id that is
        unmatched returns a 404."""
        res = self.app.delete('/api/v1/amenities/really-fake-ameni-id-001')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json.get('error'), 'Not found')

    def test_delete_amenity_id_none(self):
        """Test that attempting delete of an object whose id is None returns
        a 404."""
        res = self.app.delete('/api/v1/amenities/{}'.format(None))
        self.assertEqual(res.status_code, 404)

    def test_create_amenity(self):
        """Test that an Amenity object is created."""
        ameni_args = {'name': 'Water', 'id': 'use-this-to-delete-in-test'}
        res = self.app.post('/api/v1/amenities', json=ameni_args)
        self.assertEqual(res.status_code, 201)
        storage.delete(storage.get(Amenity, ameni_args['id']))

    def test_create_amenity_bad_data(self):
        """Test that creating an Amenity object with data that is not JSON\
        serializable returns a 400 error, with message 'Not a JSON'."""
        ameni_args = ['name', 'Bad Amenity']
        res = self.app.post('/api/v1/amenities', json=ameni_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')

    def test_create_amenity_header_not_json(self):
        """Test that creating an Amenity object when the 'Content-Type'\
        header is not set to application/json"""
        ameni_args = {'name': 'Good Amenity'}
        res = self.app.post('/api/v1/amenities',
                            content_type='application/text',
                            data=json.dumps(ameni_args))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')

    def test_create_amenity_no_name(self):
        """Test that creating an amenity without providing a name returns a\
        404 error with message, 'Missing name'."""
        ameni_args = {'amenity': 'Good'}
        res = self.app.post('/api/v1/amenities', json=ameni_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Missing name')

    def test_update_amenity(self):
        """Test that an amenity object is correctly updated."""
        ame6 = {'name': 'Amenity6'}
        ameni6 = Amenity(**ame6)
        ameni6.save()

        new_data = {'name': 'Swimming Pool'}

        self.assertEqual(storage.get(Amenity, ameni6.id).name, 'Amenity6')
        res = self.app.put('/api/v1/amenities/{}'.format(ameni6.id),
                           json=new_data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('name'), 'Swimming Pool')
        self.assertEqual(storage.get(Amenity, ameni6.id).name,
                         'Swimming Pool')
        storage.delete(ameni6)

    def test_update_amenity_bad_id(self):
        """Test that updating an amenity but the id is unmatched returns\
        a 404."""
        data = {'name': 'Updated'}
        res = self.app.put('/api/v1/amenities/does-not-exist-01',
                           json=data)
        self.assertEqual(res.status_code, 404)

    def test_update_amenity_bad_json(self):
        """Test that updating an amenity with invalid json fails with\
        code 400 and message 'Not a JSON'"""
        ame7 = {'name': 'Amenity7'}
        ame7 = Amenity(**ame7)
        ame7.save()

        new_data = ['name', 'ChangedAmenity']
        res = self.app.put('/api/v1/amenities/{}'.format(ame7.id),
                           json=new_data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')
        storage.delete(ame7)

    def test_update_amenity_wrong_content_type_value(self):
        """Test that updating the amenity object with Content-Type header\
        not set to application/json fails with 400."""
        ame8 = {'name': 'Amenity8'}
        ame8 = Amenity(**ame8)
        ame8.save()

        new_data = {'name': 'UpdatedAmenity'}
        res = self.app.put('/api/v1/amenities/{}'.format(ame8.id),
                           content_type='application/text',
                           data=json.dumps(new_data))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')
        self.assertEqual(storage.get(Amenity, ame8.id).name, 'Amenity8')
        storage.delete(ame8)

    def test_update_amenity_skipped_certain_attributes(self):
        """Test that id, created_at, and updated_at remains the same after\
        updating an amenity object."""
        ame9 = {'name': 'Amenity9', 'id': 'this-will-remain'}
        ame9 = Amenity(**ame9)
        ame9.save()

        # id attribute is enough to test that functionality
        new_data = {'name': 'NewAmenity9', 'id': 'has-been-changed'}
        res = self.app.put('/api/v1/amenities/{}'.format(ame9.id),
                           json=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('name'), new_data['name'])
        self.assertNotEqual(res.json.get('id'), new_data['id'])
        self.assertEqual(res.json.get('id'), ame9.id)
        storage.delete(ame9)
