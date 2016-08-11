#!venv/bin/python3

import os
import unittest
import bcrypt

from config import basedir
from app import app, db
from app.models import Vehicle, GasStop

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

    def test_passwd(self):
        passwd = bcrypt.hashpw(b'Testing', bcrypt.gensalt())
        v = Vehicle(name='Ranger', passwd=passwd)
        assert v.passwd == bcrypt.hashpw(b'Testing', passwd)

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