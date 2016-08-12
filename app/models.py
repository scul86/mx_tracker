from app import db, app
from bcrypt import hashpw, gensalt

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    passwd_hash = db.Column(db.String(128))
    mileage = db.Column(db.DECIMAL, index=True)
    gas_stop = db.relationship('GasStop', backref='vehicle', lazy='dynamic')
    # maint = db.relationship('Maintenance', backref='vehicle', lazy='dynamic')
    # about_me = db.Column(db.String(140))
    last_updated = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('passwd is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwd_hash = hashpw(password.encode('utf-8'), gensalt())

    def verify_passwd(self, password):
        return self.passwd_hash == hashpw(password.encode('utf-8'), self.passwd_hash)

    @staticmethod
    def make_unique_name(name):
        if Vehicle.query.filter_by(name=name).first() is None:
            return name
        version = 2
        while True:
            new_name = name + str(version)
            if Vehicle.query.filter_by(name=new_name).first() is None:
                break
            version += 1
        return new_name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<Vehicle {}>'.format(self.name)


class GasStop(db.Model):
    # __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    gallons = db.Column(db.DECIMAL)
    price = db.Column(db.DECIMAL)
    trip = db.Column(db.DECIMAL)
    mpg = db.Column(db.DECIMAL)
    location = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return '<GasStop {}>'.format(self.id)
