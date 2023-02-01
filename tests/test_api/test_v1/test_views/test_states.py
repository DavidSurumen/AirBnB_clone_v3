#!/usr/bin/python3
"""Test module for states view"""
import unittest
from api.v1.app import app
from models.state import State
import json
from models import storage


class TestStateView(unittest.TestCase):
    """Test cases for all routes in states.py"""
    @classmethod
    def setUpClass(cls):
        """set the flask app in testing mode."""
        app.config['TESTING'] = True
        cls.app = app.test_client()

    def test_getstates(self):
        """Test that the route /states retrieves all State objects."""
        state_args = {'name': 'Nakuru'}
        state = State(**state_args)
        state.save()

        res = self.app.get('/api/v1/states/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(res.get_data(), encoding="utf-8"))

        self.assertTrue(type(json_format), list)
        self.assertIn(state_args["name"], [st.get("name")
                                           for st in json_format])
        storage.delete(state)

    def test_getstate(self):
        """Test that the route /states/<state_id> returns one State object
        by its id."""
        state_args = {"name": "Nakuru", "id": "naks2023"}
        state = State(**state_args)
        state.save()

        res = self.app.get("/api/v1/states/{}".format(state_args["id"]))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(res.get_data(), encoding="utf-8"))

        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_getstate_false(self):
        """Test that GET /states/<state_id> with an id that does not exist
        returns 404"""
        state_args = {"name": "Nakuru", "id": "fake-state-2023"}
        state = State(**state_args)
        state.save()

        res = self.app.get('/api/v1/states/{}/'.format("fake-id-wkkeo-2339"))

        self.assertEqual(res.status_code, 404)
        storage.delete(state)

    def test_deletestate(self):
        """Tests that the route /states/<state_id> for DELETE correctly
        removes an object from storage."""
        state_args = {"name": "Nakuru", "id": "nakuru-kenya-2023"}
        state = State(**state_args)
        state.save()

        res = self.app.delete("/api/v1/states/{}".format(state_args["id"]))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(res.get_data(), encoding="utf-8"))

        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get('State', state_args["id"]))

    def test_deletestate_wrong_id(self):
        """Tests that DELETE /states/<state_id> with unmatched state id
        returns 404"""
        state_args = {"name": "Nairobi", "id": "kanairo23"}
        state = State(**state_args)
        state.save()

        res = self.app.delete('/api/v1/states/{}'.format("fake-id-23"))

        self.assertEqual(res.status_code, 404)
        storage.delete(state)

    def test_createstate(self):
        """Test that POST /states creates a new state object."""
        state_args = {"name": "Mombasa", "id": "pwani23"}

        res = self.app.post('api/v1/states', json=state_args)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(res.get_data(), encoding="utf-8"))

        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])

        st = storage.get(State, state_args["id"])

        self.assertIsNotNone(st)
        storage.delete(st)

    def test_createstate_bad_json(self):
        """Test creating a state object with invalid json"""
        state_args = {"name": "Mombasa"}

        res = self.app.post('/api/v1/states', data=state_args)
        self.assertEqual(res.status_code, 400)

        self.assertEqual(res.json.get("message"), "Not a JSON")

        res = self.app.post("/api/v1/states",
                            content_type="application/x-www-form-urlencoded",
                            data=json.dumps(state_args))
        self.assertEqual(res.status_code, 400)

    def test_createstate_no_name(self):
        """Test creating a state without a name"""
        state_args = {'id': 'no-name'}

        res = self.app.post('/api/v1/states', content_type="application/json",
                            data=json.dumps(state_args))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Missing name")

    def test_updatestate(self):
        """Test that a State object in storage is updated."""
        state_args = {"name": "Free State", "id": "update-me-2023"}
        state = State(**state_args)
        state.save()

        new_data = {"name": "Updated State"}
        res = self.app.put('/api/v1/states/{}'.format(state_args["id"]),
                           json=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(res.get_data(), encoding="utf-8"))
        self.assertEqual(json_format.get("name"), new_data["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])

        storage.delete(state)

    def test_updatestate_bad_json(self):
        """Test that updating a stored object with invalid json returns a 400
        with the message 'Not a JSON'
        """
        state_args = {"name": "Some State", "id": "some id"}
        state = State(**state_args)
        state.save()

        bad_json = ["name", "Failed State"]
        res = self.app.put('/api/v1/states/{}'.format(state_args["id"]),
                           json=bad_json)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json.get("message"), "Not a JSON")
        storage.delete(state)

    def test_updatestate_bad_id(self):
        """Test that updating a stored object with umatching id returns a 404
        status code."""
        state_args = {"name": "Not Update", "id": "some-id-23"}
        state = State(**state_args)
        state.save()

        new_data = {"name": "Updated", "id": "new-id-23"}
        res = self.app.put('/api/v1/states/{}'.format('a-false-id-494fj99sd'),
                           json=new_data)
        self.assertEqual(res.status_code, 404)

        obj = storage.get(State, state_args["id"])

        self.assertEqual(obj.name, state.name)
        self.assertEqual(obj.id, state.id)
        storage.delete(obj)


if __name__ == "__main__":
    unittest.main()
