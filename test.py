#!venv/bin/python3

import os
import unittest

from config import basedir
from app import app, db
from app.models import Vehicle, GasStop
from datetime import datetime

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_vehicle_password_setter(self):
        v = Vehicle(password='Testing Password')
        self.assertTrue(v.password_hash is not None)

    def test_no_password_getter(self):
        v = Vehicle(password='Testing Password')
        with self.assertRaises(AttributeError):
            v.password

    def test_password_verification(self):
        v = Vehicle(password='Testing Password')
        self.assertTrue(v.verify_password('Testing Password'))
        self.assertFalse(v.verify_password('Wrong Password'))

    def test_password_salts_are_random(self):
        v1 = Vehicle(password='password')
        v2 = Vehicle(password='password')
        self.assertTrue(v1.password_hash != v2.password_hash)

    def test_is_authenticated(self):
        v = Vehicle()
        self.assertTrue(v.is_authenticated)

    def test_is_active(self):
        v = Vehicle()
        self.assertTrue(v.is_active)

    def test_is_anonymous(self):
        v = Vehicle()
        self.assertFalse(v.is_anonymous)

    def test_gas_stop(self):
        v = Vehicle(name='Ranger')
        GasStop(gallons=10.5,
                price=1.25,
                trip=123.45,
                vehicle=v)
        stop = v.gas_stop.all()[0]
        stop.mpg = stop.trip/stop.gallons
        assert stop.gallons == 10.5
        assert stop.price == 1.25
        assert stop.trip == 123.45
        assert stop.mpg == 123.45/10.5
        assert stop.vehicle.name == 'Ranger'

if __name__ == '__main__':
    unittest.main()
