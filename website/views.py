from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, session, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import requests
from .forms import *
from .crud import *

views = Blueprint("views", __name__)


@views.route('/', defaults={'path': ''})
@views.route('/<string:path>')
@views.route('/<path:path>')
def catch_random_paths(path):
    """
    Catches all URL paths that aren't specified and sends to the home page.
    """
    return redirect(url_for("views.welcome"))


@views.route('/', methods=['POST', 'GET'])
def welcome():
    if not User.query.filter_by(username="admin").first(): 
        initialize_test_devices_and_admin() 
    login_form = LoginForm()
    return render_template("welcome.html", login_form=login_form)

# Rejestracja nowych uzytkownikow + TESTOWA inicjacja wstepnych danych do bazy danych (diody ustawione na False i jakas temperatura)
@views.route('/admin-register', methods=['POST', 'GET'])
@login_required
def admin_register():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template("welcome_register.html", login_form=login_form, register_form=register_form)


@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template("home.html")

@views.route('/register', methods=["POST", "GET"])
@login_required
def register():
    register_form = RegisterForm()
    if request.method == "POST":
        print(register_form.password.data)
        print(register_form.confirm_password.data)
        user = User.query.filter_by(username=register_form.username.data).first()
        if user:
            flash(u"Istnieje już użytkownik o takiej nazwie", 'error')
            return '<script>document.location.href = document.referrer</script>'
        if register_form.password.data != register_form.confirm_password.data:
            flash(u"Hasła sie są takie same", 'error')
            return '<script>document.location.href = document.referrer</script>'

        else:
            
            hash_and_salted_password = generate_password_hash(
                register_form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user = create_user(
                register_form.username.data,
                hash_and_salted_password,
            )

            login_user(user)
            flash(u'Stworzono nowe konto!', 'success')
            return '<script>document.location.href = document.referrer</script>'
    return redirect(url_for('views.home'))


@views.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        print("working login")
        print(login_form.username.data)
        username = login_form.username.data
        password = login_form.password.data

  
        user = User.query.filter_by(username=username).first()

     
        if not user:
            flash(u"Użytkownik nie istnieje", 'error')
            return '<script>document.location.href = document.referrer</script>'
    
        elif not check_password_hash(user.password, password):
            flash(u'Niepoprawne hasło', 'error')
            return '<script>document.location.href = document.referrer</script>'
       
        else:
            login_user(user)
    return redirect(url_for("views.home"))


@views.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
    return redirect(url_for("views.welcome"))

############################################################################################################


@views.route("/devices_info", methods=['POST', 'GET'])
@login_required
def devices_info():
    return render_template("devices_info.html")

@views.route("/devices_control", methods=['POST', 'GET'])
@login_required
def devices_control():
    return render_template("devices_control.html")
@login_required

@views.route("/lock", methods=['POST', 'GET'])
@login_required
def lock():
    return render_template("devices/lock.html")

@views.route("/leds", methods=['POST', 'GET'])
@login_required
def leds():
    return render_template("devices/LEDs.html")

@views.route("/temperature", methods=['POST', 'GET'])
@login_required
def temperature():
    return render_template("devices/temperature.html")

@views.route("/humidity", methods=['POST', 'GET'])
@login_required
def humidity():
    return render_template("devices/humidity.html")

@views.route('/check_led_status', methods=['GET'])
@login_required
def check_led_status():
    led_status_1 = get_device_state("dioda_1")
    led_status_2 = get_device_state("dioda_2")
    led_status_3 = get_device_state("dioda_3")
    
    print(led_status_1)
    print(led_status_2)
    print(led_status_3)
    return jsonify({'led_status_1': led_status_1, 'led_status_2': led_status_2, 'led_status_3': led_status_3})



@views.route('/toggle_led_state', methods=['POST'])
@login_required
def toggle_led_state_view():
    data = request.get_json()
    device_name = data.get('device_name')
    toggle_device_state(device_name)
    return 200
    
@views.route('/check_lock_status', methods=['GET'])
@login_required
def check_lock_status():
    lock_status_1 = get_device_state("zamek_1")
    
    print(lock_status_1)
    return jsonify({'lock_status_1': lock_status_1})


@views.route('/toggle_lock_state', methods=['POST'])
@login_required
def toggle_lock_state_view():
    data = request.get_json()
    device_name = data.get('device_name')
    toggle_device_state(device_name)
    return 200



@views.route('/get_temperature', methods=['GET'])
def get_temperature():
    temperature = get_temperature_state("temp_sensor_1")
    print(temperature)
   
    return jsonify({'temperature': temperature})


@views.route('/get_humidity', methods=['GET'])
def get_humidity():
    humidity = get_humidity_state("humidity_sensor_1")
    print(humidity)
   
    return jsonify({'humidity': humidity})