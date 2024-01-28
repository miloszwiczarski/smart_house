from . import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Device(db.Model):
    __tablename__ = 'Devices'
    device_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    is_on = db.Column(db.Boolean, nullable=False)

    def get_state(self):
        return self.is_on


class TemperatureSensor(db.Model):
    __tablename__ = 'temperature_sensor'
    device_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)

class HumiditySensor(db.Model):
    __tablename__ = 'humidity'
    device_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
