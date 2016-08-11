#!venv/bin/python3

from app import models, db
from datetime import datetime

import bcrypt

passwd = bcrypt.hashpw(b'Testing', bcrypt.gensalt())

v = models.Vehicle(name='Ranger')
print('Prior to add(v)')
db.session.add(v)
print('Prior to commit()')
db.session.commit()

input('Press Enter')