#!/usr/bin/python3
"""Test module for users view."""
import unittest
from api.v1.app import app
from models.user import User
from models import storage
import json


class TestUserView(unittest.TestCase):
    """Test cases for all the routes in the users.py module."""
    @classmethod
    def setUpClass(cls):
        """set up the flask app in testing mode."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

    def test_get_users(self):
        """Test that a list of all users is retrieved correctly."""
        user1 = {'email': 'Email1', 'password': 'Pass1'}
        user1 = User(**user1)
        user1.save()
        user2 = {'email': 'Email2', 'password': 'Pass2'}
        user2 = User(**user2)
        user2.save()

        self.assertEqual(storage.get(User, user1.id), user1)
        res = self.app.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')
        self.assertTrue(type(res.json), list)

        all_users = res.json
        self.assertIn(user1.email, [user.get('email') for user in all_users])
        self.assertIn(user2.password, [user.get('password') for user
                                       in all_users])

        storage.delete(user1)
        storage.delete(user2)

    def test_get_users_single_user(self):
        """Test that a single user can be retrieved."""
        user3 = {'email': 'Email3', 'password': 'Pass3'}
        user3 = User(**user3)
        user3.save()

        res = self.app.get('/api/v1/users/{}'.format(user3.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('email'), user3.email)
        storage.delete(user3)

    def test_delete_user(self):
        """Test that a user object is deleted."""
        user4 = {'email': 'Email4', 'password': 'pass4'}
        user4 = User(**user4)
        user4.save()

        self.assertIsNotNone(storage.get(User, user4.id))
        res = self.app.delete('/api/v1/users/{}'.format(user4.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {})
        self.assertIsNone(storage.get(User, user4.id))

    def test_delete_user_bad_id(self):
        """Test that trying to delete a user object whose id does not exist\
        returns a 404."""
        res = self.app.delete('/api/v1/users/this-does-not-exist-001')
        self.assertEqual(res.status_code, 404)

    def test_create_user(self):
        """Test that a user object is created."""
        user_args = {'email': 'email@user5', 'password': 'pass5'}
        res = self.app.post('/api/v1/users', json=user_args)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json.get('email'), user_args['email'])

        id = res.json.get('id')
        storage.delete(storage.get(User, id))

    def test_create_user_invalid_json(self):
        """Test that creating user object with invalid json returns a 400\
        with 'Not a JSON'"""
        user_args = ['email', 'fails']
        res = self.app.post('/api/v1/users', json=user_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')

    def test_create_user_wrong_header_type(self):
        """Test that creating a user with a request whose content-type header\
        is not application/json fails with 400 and 'Not a JSON'"""
        user_args = {'email': 'Loftus', 'password': 'cheek'}
        res = self.app.post('/api/v1/users',
                            content_type='application/text',
                            data=json.dumps(user_args))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Not a JSON')

    def test_create_user_no_email(self):
        """Test that creating a user without an email fails with 400\
        and 'Missing email'"""
        user_args = {'firstname': 'User6', 'password': 'pass6'}
        res = self.app.post('/api/v1/users', json=user_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Missing email')

    def test_create_user_no_password(self):
        """Test that creating a user without a password fails with 400\
        and 'Missing password'"""
        user_args = {'firstname': 'User7', 'email': 'email@user7'}
        res = self.app.post('/api/v1/users', json=user_args)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get('message'), 'Missing password')

    def test_update_user(self):
        """Test that a User object is updated with new values."""
        user8 = {'first_name': 'User8', 'email': 'email@user8',
                 'password': 'pass8'}
        user8 = User(**user8)
        user8.save()

        new_vals = {'first_name': 'NewName'}
        res = self.app.put('/api/v1/users/{}'.format(user8.id),
                           json=new_vals)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, user8.to_dict())
        storage.delete(user8)

    def test_update_user_bad_id(self):
        """Test that updating a user whose id does not exist fails with 400.
        """
        new_dat = {'first_name': 'Assigned'}
        res = self.app.put('/api/v1/users/un-match-ing-id-023', json=new_dat)
        self.assertEqual(res.status_code, 404)

    def test_update_user_bad_json(self):
        """Test that updating a user with invalid json fails with 400 and \
        'Not a JSON'"""
        user9 = {'email': 'email@user9', 'password': 'pass9'}
        user9 = User(**user9)
        user9.save()

        self.assertEqual(storage.get(User, user9.id).password, 'pass9')
        new_dat = ['password', 'new-pass9']
        res = self.app.put('/api/v1/users/{}'.format(user9.id), json=new_dat)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Not a JSON")
        self.assertEqual(storage.get(User, user9.id).password, 'pass9')
