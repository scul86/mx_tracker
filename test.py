#!venv/bin/python3

import os
import unittest
import bcrypt

from config import basedir
from app import app, db
from app.models import Vehicle, GasStop
from datetime import datetime

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_name(self):
        v = Vehicle(name='Testing')
        assert v.name == 'Testing'

    def test_passwd(self):
        passwd = 'Testing'.encode('utf-8')
        passwd = bcrypt.hashpw(passwd, bcrypt.gensalt())
        v = Vehicle(passwd=passwd)
        assert v.passwd == bcrypt.hashpw(b'Testing', passwd)

    def test_mileage(self):
        v = Vehicle(mileage=10.90)
        assert v.mileage == 10.9

    def test_last_update(self):
        time = datetime.utcnow()
        v = Vehicle(last_updated=time)
        assert v.last_updated == time

if __name__ == '__main__':
    unittest.main()

'''
v = Vehicle(name='Ranger')
print('Prior to add(v)')
db.session.add(v)
print('Prior to commit()')
db.session.commit()

input('Press Enter')
'''