#!venv/bin/python3

from app import models, db
from datetime import datetime

import bcrypt

passwd = bcrypt.hashpw(b'Testing', bcrypt.gensalt())

v = models.Vehicle(name='Ranger')
db.session.add(v)
db.session.commit()

input('Press Enter')