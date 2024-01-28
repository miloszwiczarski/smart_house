"""CRUD operations
Create, Read, Update, Delete."""

from .models import db, User, Device, TemperatureSensor, HumiditySensor
from website import db
from website.models import Device, TemperatureSensor, HumiditySensor, User
from werkzeug.security import generate_password_hash



# ***** User class crud functions *****

def create_user(username, password):
    """Create a user."""

    # Instantiate a User
    user = User(username=username, password=password)

    # add new instance of user to db and commit
    db.session.add(user)
    db.session.commit()

    return user


def get_device_state(name):
    device = db.session.query(Device).filter_by(name=name).first()
    if device:
        return device.is_on
    else:
        return False  


def get_temperature_state(name):
    temperature_sensor = TemperatureSensor.query.filter_by(name=name).first()
    if temperature_sensor:
        return temperature_sensor.value
    else:
        return None 
    
def get_humidity_state(name):
    humidity_sensor = HumiditySensor.query.filter_by(name=name).first()
    if humidity_sensor:
        return humidity_sensor.value
    else:
        return None  

def toggle_device_state(device_name):

    device = Device.query.filter_by(name=device_name).first()
    if device:
       
        device.is_on = not device.is_on 
     
        db.session.commit()
        return True 
    else:
        return False


def initialize_test_devices_and_admin():
    """Initialize test devices and data."""
    
    devices = [
        {'name': 'dioda_1', 'is_on': False},
        {'name': 'dioda_2', 'is_on': False},
        {'name': 'dioda_3', 'is_on': False},
        {'name': 'zamek_1', 'is_on': False},
        {'name': 'lampa_1', 'is_on': False}
    ]

    for device_data in devices:
        device = Device(name=device_data['name'], is_on=device_data['is_on'])
        db.session.add(device)

 
    temperature = TemperatureSensor(name='temp_sensor_1', value=20.5)
    db.session.add(temperature)

    
    humidity = HumiditySensor(name='humidity_sensor_1', value=0.5)
    db.session.add(humidity)

    hash_and_salted_password = generate_password_hash(
                    "admin",
                    method='pbkdf2:sha256',
                    salt_length=8
                )
    create_user(
                    "admin",
                    hash_and_salted_password,
                )

    # Commit all changes to the database
    db.session.commit()

    print("Test devices and data initialized successfully.")



